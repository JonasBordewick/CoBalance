#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: simulation_job_factory.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from app.domain.simulation import SimulationJob


class SimulationJobFactory:

    @staticmethod
    def create_simulation_jobs(unity_application_path: str, project_path: str, job_file_path: str) -> SimulationJob:
        return SimulationJob(
                unity_application_path,
                project_path,
                job_file_path,
            )