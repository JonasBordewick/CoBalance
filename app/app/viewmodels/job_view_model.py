#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: job_view_model.py
Author: Jonas Bordewick
Date: 21.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import json
import os

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

from app.domain.simulation import SimulationJobFactory
from app.io.repositories import JobRepository
from app.models import ProjectSettings, ParameterTableRow
from app.models.job_settings import JobSettings

from app.workers import SimulationWorker, GeneticAlgorithmWorker
from .project_context_view_model import ProjectContextViewModel
from ..domain.auto_suggestion import AutoSuggestionSettings
from ..io.watchers import DirectoryWatcherService


class JobViewModel(QObject):
    file_watcher_key_progress = "progress"

    state_changed = pyqtSignal()

    simulation_started = pyqtSignal()
    simulation_finished = pyqtSignal()
    simulation_log = pyqtSignal(str)
    simulation_progress = pyqtSignal(int, int)   # current_run, total_runs

    auto_suggestion_started = pyqtSignal()
    auto_suggestion_finished = pyqtSignal()
    auto_suggestion_progress = pyqtSignal(int, int)  # current_generation, total_generations

    job_progress = pyqtSignal(str)

    # Signals for Auto Suggestion
    selected_parameters_changed = pyqtSignal()

    def __init__(
            self,
            project_context_view_model: ProjectContextViewModel,
            file_watcher: DirectoryWatcherService,
            parent=None
    ):
        super().__init__(parent)
        self.jobs_dir: str | None = None
        self._thread: QThread | None = None
        self._worker: SimulationWorker | None = None
        self._ga_worker: GeneticAlgorithmWorker | None = None
        self._is_running = False
        self._last_error: str | None = None
        self._total_generations: int = 0

        self._selected_parameter_rows: list[ParameterTableRow] = []

        self._project_context_view_model = project_context_view_model
        self._project_context_view_model.project_changed.connect(
            self.set_jobs_dir
        )
    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def selected_parameter_rows(self) -> list[ParameterTableRow]:
        return self._selected_parameter_rows

    def set_jobs_dir(self):
        self.jobs_dir = self._project_context_view_model.jobs_directory

    def select_parameters(self, parameters: list[ParameterTableRow]):
        self._selected_parameter_rows = parameters
        self.selected_parameters_changed.emit()

    def start_simulation(
        self,
        project_settings: ProjectSettings,
        job_settings: JobSettings
    ) -> None:
        if self._is_running:
            self.simulation_log.emit("A simulation is already running.")
            return

        if not self.jobs_dir:
            self._project_context_view_model.on_error("jobs_dir is not set.")
            return

        if not project_settings.unity_application_path:
            self._project_context_view_model.on_error("Unity application path is not set.")
            return

        if not project_settings.project_path:
            self._project_context_view_model.on_error("Project path is not set.")
            return

        job_file_path = os.path.join(self.jobs_dir, f"job_{job_settings.job_id}.json")
        JobRepository.save_job_settings_to_file(job_settings, job_file_path)

        job = SimulationJobFactory.create_simulation_jobs(
            unity_application_path=project_settings.unity_application_path,
            project_path=project_settings.project_path,
            job_file_path=job_file_path,
        )

        self._worker = SimulationWorker(job=job)
        self._worker.progress_changed.connect(self.simulation_progress)

        self._is_running = True
        self.state_changed.emit()
        self.simulation_started.emit()
        self._start_worker_in_thread(self._worker)

    def start_auto_suggestion(self, settings: AutoSuggestionSettings, project_settings: ProjectSettings):
        if self._is_running:
            self.simulation_log.emit("Another job is already running.")
            return

        self._total_generations = settings.generation_count
        self._ga_worker = GeneticAlgorithmWorker(
            progress_file_path=self._project_context_view_model.progress_file_path,
            jobs_directory_path=self.jobs_dir,
            balance_directory_path=self._project_context_view_model.balances_directory,
            project_settings=project_settings,
            settings=settings
        )
        self._ga_worker.progress_changed.connect(self._on_ga_progress)

        self._is_running = True
        self.state_changed.emit()
        self.auto_suggestion_started.emit()
        self._start_worker_in_thread(self._ga_worker)

    def _start_worker_in_thread(self, worker: QObject) -> None:
        """
        Moves a worker onto a new QThread and wires up the standard Qt
        worker/thread lifecycle signals.

        Signal order matters here:
        1. worker.finished/failed → thread.quit   (ask the event loop to stop)
        2. worker.finished/failed → worker.deleteLater  (schedule worker cleanup)
        3. worker.finished/failed → _on_worker_finished/_on_worker_failed
           (update UI state while the thread is still alive)
        4. thread.finished → _on_thread_finished  (clear references only after
           the thread has fully stopped — avoids "destroyed while running" errors)
        5. thread.finished → thread.deleteLater   (schedule thread cleanup last)

        Connecting _on_thread_finished to thread.finished (not worker.finished)
        is critical: the thread may still be processing after the worker emits
        finished, so dereferencing it too early would cause a Qt crash.
        """
        self._thread = QThread()
        worker.moveToThread(self._thread)

        self._thread.started.connect(worker.run)

        worker.finished.connect(self._thread.quit)
        worker.failed.connect(self._thread.quit)

        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)

        worker.finished.connect(self._on_worker_finished)
        worker.failed.connect(self._on_worker_failed)

        # Connect cleanup to thread.finished, NOT worker.finished, so the thread
        # object is only dereferenced once the OS thread has actually exited.
        self._thread.finished.connect(self._on_thread_finished)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    @pyqtSlot(int)
    def _on_ga_progress(self, generation: int):
        # The worker emits 0-based generation indices; convert to 1-based for display.
        self.auto_suggestion_progress.emit(generation + 1, self._total_generations)

    def _on_worker_finished(self):
        self._is_running = False
        self.state_changed.emit()

    def _on_worker_failed(self, message: str):
        self._last_error = message
        self._project_context_view_model.on_error(message)
        self._is_running = False
        self.state_changed.emit()

    def _on_thread_finished(self):
        # _last_error is set by _on_worker_failed (which fires before thread.finished),
        # so we can safely read it here to decide whether to report an error or
        # emit the success signal.
        error = self._last_error

        self._worker = None
        self._ga_worker = None
        self._thread = None
        self._last_error = None

        if error:
            self._project_context_view_model.on_error(error)
        else:
            self.simulation_finished.emit()



