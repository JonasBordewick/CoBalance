#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: genetic_algorithm_worker.py
Author: Jonas Bordewick
Date: 01.04.26
Contact: jonas.bordewick@uni-a.de
"""
import json
import os
import random

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from app.domain.auto_suggestion import AutoSuggestionSettings, Candidate
from app.domain.simulation import SimulationJob
from app.io.process import UnitySimulationRunner
from app.io.repositories import BalanceRepository, JobRepository
from app.models import ProjectSettings, BalanceFile
from app.models.job_settings import JobSettings


class GeneticAlgorithmWorker(QObject):
    progress_changed = pyqtSignal(int) # generation

    finished = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(
            self,
            progress_file_path: str,
            jobs_directory_path: str,
            balance_directory_path: str,
            settings: AutoSuggestionSettings,
            project_settings: ProjectSettings
    ):
        super().__init__()
        self.progress_file_path = progress_file_path
        self.jobs_directory_path = jobs_directory_path
        self.balance_directory_path = balance_directory_path
        self.settings = settings
        self.project_settings = project_settings
        self._cancel_requested = False
        self._runner = UnitySimulationRunner()

    @pyqtSlot()
    def run(self):
        """
        Main loop of the genetic algorithm.

        Each generation evaluates the entire population in a single batched Unity
        simulation run. Candidates that already carry a fitness score (elites carried
        over from the previous generation) are skipped in the batch to avoid
        re-simulating them. After evaluation the population is sorted by fitness and
        a new generation is bred via crossover and mutation.

        After all generations are done, the top-k elite individuals are written to
        the balance output directory as separate JSON files.
        """
        try:
            population = self._create_initial_population()

            for generation in range(self.settings.generation_count):
                if self._cancel_requested:
                    self.finished.emit()
                    return

                run_dir = os.path.join(
                    self.jobs_directory_path,
                    "auto_suggestion",
                    self.settings.snapshot_id,
                    f"gen_{generation:04d}"
                )
                os.makedirs(run_dir, exist_ok=True)
                result_file_path = os.path.join(run_dir, "result.json")
                job_file_path = os.path.join(run_dir, "job.json")

                # Only write balance files for candidates without a fitness score yet.
                # Elites carried over from the last generation already have one.
                balances = self._create_population_balances_of_generation(population, generation, run_dir)

                self.progress_changed.emit(generation)

                job_settings = JobSettings(
                    version="1.0",
                    job_type="geneticAlgorithm",
                    job_id=f"ga_{self.settings.snapshot_id}_gen_{generation:04d}",
                    input_settings={
                        "scenePath": self.settings.scene_path,
                        "balanceFilePaths": balances,
                        "resultFilePath": result_file_path,
                        "iterationsPerBalanceFile": self.settings.runs_per_individual,
                        "progressFilePath": self.progress_file_path
                    },
                    execution_settings={
                        "timeScale": self.settings.time_scale,
                        "fixedDeltaTime": 0.02,
                        "maxSimulationTime": self.settings.max_time,
                    }
                )

                JobRepository.save_job_settings_to_file(job_settings, job_file_path)

                job = SimulationJob(
                    unity_application_path=self.project_settings.unity_application_path,
                    project_path=self.project_settings.project_path,
                    job_file_path=job_file_path,
                    create_logs=False
                )

                result = self._runner.run(job)

                if not result.success:
                    self.failed.emit(f"Genetic Algorithm exited with exit code {result.exit_code}!")
                    return

                with open(result_file_path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)

                # The result file maps candidate_id → list of per-run scores.
                # Average them to get a single fitness value per candidate.
                for candidate_id in data:
                    fitness = sum(data[candidate_id]) / len(data[candidate_id])
                    for candidate in population:
                        if candidate.id == candidate_id:
                            candidate.fitness = fitness
                            break

                # Sort descending so index 0 is always the best individual.
                population.sort(key=lambda c: c.fitness or float("-inf"), reverse=True)

                population = self._build_next_generation(population, generation + 1)

            # Save the top-k elite candidates as output balance files.
            for idx, top_candidate in enumerate(population[:self.settings.elite_count]):
                top_balance = self._build_balance(top_candidate)
                file_name = f"{self.settings.snapshot_id}_{idx}.json"
                BalanceRepository.save_balance_to_file(top_balance, os.path.join(self.balance_directory_path, file_name))

            self.finished.emit()
        except Exception as e:
            self.failed.emit(str(e))

    def cancel(self):
        self._cancel_requested = True
        self._runner.cancel()

    def _build_balance(self, candidate: Candidate) -> BalanceFile:
        balance = BalanceRepository.load_balance_from_file(
            self.settings.base_balance_file_path
        )

        for key, value in candidate.genes.items():
            balance.values[key] = value

        return balance

    def _create_population_balances_of_generation(self, population: list[Candidate], generation: int, run_dir: str) -> list[str]:
        files: list[str] = []

        for candidate_idx, candidate in enumerate(population):

            if candidate.fitness:
                continue

            balance = self._build_balance(candidate)
            balance_file_path = os.path.join(run_dir, f"{candidate.id}_balance.json")

            BalanceRepository.save_balance_to_file(balance, balance_file_path)
            files.append(balance_file_path)

        return files


    def _evaluate_candidate(self, candidate: Candidate, generation: int, candidate_idx: int) -> float:

        if candidate.fitness:
            return candidate.fitness

        balance = self._build_balance(candidate)

        run_dir = os.path.join(
            self.jobs_directory_path,
            "auto_suggestion",
            self.settings.snapshot_id,
            f"gen_{generation:04d}",
            f"cand_{candidate_idx:04d}"
        )
        os.makedirs(run_dir, exist_ok=True)

        balance_file_path = os.path.join(run_dir, "balance.json")
        result_file_path = os.path.join(run_dir, "result.json")
        job_file_path = os.path.join(run_dir, "job.json")

        BalanceRepository.save_balance_to_file(balance, balance_file_path)

        job_settings = JobSettings(
            version="1.0",
            job_type="simulation",
            job_id=f"ga_g{generation}_c{candidate_idx}",
            input_settings={
                "scenePath": self.settings.scene_path,
                "balanceFilePath": balance_file_path,
                "resultFilePath": result_file_path,
            },
            execution_settings={
                "timeScale": self.settings.time_scale,
                "fixedDeltaTime": 0.02,
                "maxSimulationTime": self.settings.max_time,
            }
        )

        JobRepository.save_job_settings_to_file(job_settings, job_file_path)

        job = SimulationJob(
            unity_application_path=self.project_settings.unity_application_path,
            project_path=self.project_settings.project_path,
            job_file_path=job_file_path,
            create_logs=False
        )

        results = []

        for _ in range(self.settings.runs_per_individual):
            result = self._runner.run(job)
            if not result.success:
                results.append(float("-inf"))
                continue

            try:
                with open(result_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results.append(data["fitness"])
            except Exception as e:
                # results.append(float("-inf"))
                results.append(random.uniform(0, 100))

        return sum(results) / len(results)


    def _create_initial_population(self) -> list[Candidate]:
        population = []
        for i in range(self.settings.population_size):
            genes = {}
            for param in self.settings.parameter_settings:
                value = random.uniform(param.value_min, param.value_max)
                if param.parameter_type == "int":
                    value = int(round(value))
                genes[param.parameter_key] = value
            population.append(Candidate(genes=genes, id=f"gen_0000_cand_{i:04d}"))
        return population

    def _build_next_generation(self, population: list[Candidate], generation_idx: int) -> list[Candidate]:
        """
        Builds the next generation using elitism + crossover + mutation.

        The top-k elite candidates are copied unchanged so the best solution found
        so far is never lost. The rest of the generation is filled by selecting two
        parents from the parent pool via tournament selection, blending their genes,
        and then applying random mutations.

        The parent pool is capped at max(10, elite_count) to keep selection pressure
        high: only fit individuals compete to produce offspring.
        """
        top_count = self.settings.elite_count

        # Elites: carry over the best individuals with their fitness intact so they
        # are not re-evaluated in the next generation's batch.
        next_population = [
            Candidate(genes=dict(c.genes), fitness=c.fitness, id=c.id)
            for c in population[:top_count]
        ]

        # Restrict parent selection to the top of the population to maintain
        # selection pressure while still allowing some diversity.
        pool_size = max(10, top_count)
        if pool_size >= len(population):
            pool_size = len(population)

        parent_pool = population[:pool_size]

        counter = 0

        while len(next_population) < self.settings.population_size:
            p1 = GeneticAlgorithmWorker.tournament_selection(parent_pool)
            p2 = GeneticAlgorithmWorker.tournament_selection(parent_pool)

            child = GeneticAlgorithmWorker.blend_crossover(p1, p2, generation_idx, counter)
            self._mutate(child)

            next_population.append(child)
            counter += 1

        return next_population

    def _mutate(self, candidate: Candidate):
        """
        Applies random mutations to a candidate's genes in-place.

        Each gene is mutated independently with a fixed probability. The new value
        is clamped to [value_min, value_max] so it always stays within the
        user-defined search bounds.
        """
        mutation_rate = 0.2

        for p in self.settings.parameter_settings:
            if random.random() >= mutation_rate:
                continue

            current = candidate.genes[p.parameter_key]

            delta = random.uniform(-p.mutation_step, p.mutation_step)
            new_value = current + delta
            # Clamp to the configured search bounds.
            new_value = max(p.value_min, min(p.value_max, new_value))

            if p.parameter_type == "int":
                new_value = int(round(new_value))

            candidate.genes[p.parameter_key] = new_value

    @staticmethod
    def crossover(parent1: Candidate, parent2: Candidate) -> Candidate:
        child_genes = {}
        for key in parent1.genes.keys():
            child_genes[key] = random.choice([parent1.genes[key], parent2.genes[key]])
        return Candidate(genes=child_genes)

    @staticmethod
    def blend_crossover(parent1: Candidate, parent2: Candidate, generation: int, candidate_idx: int) -> Candidate:
        """
        Uniform blend crossover: every gene of the child is a weighted average of
        the two parents' genes using the same random weight α ∈ [0, 1].

        Using a single α per child (rather than per-gene) preserves gene correlations
        between parameters while still producing offspring that differ from both parents.
        """
        a = random.random()
        child_genes = {}
        for key in parent1.genes.keys():
            child_genes[key] = a * parent1.genes[key] + (1 - a) * parent2.genes[key]
        return Candidate(genes=child_genes, id=f"gen_{generation:04d}_cand_{candidate_idx:04d}")

    @staticmethod
    def tournament_selection(population: list[Candidate], k=3) -> Candidate:
        """
        Selects one parent via k-tournament selection.

        k candidates are drawn at random and the one with the highest fitness wins.
        Candidates without a fitness score (fitness=None) are treated as worst-case
        (float("-inf")) so unevaluated individuals cannot accidentally win a tournament.
        """
        selection = random.sample(list(population), k=k)
        selection.sort(key=lambda c: c.fitness or float("-inf"), reverse=True)
        return selection[0]

