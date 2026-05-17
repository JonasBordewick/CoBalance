#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: simulation_models.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import datetime
from dataclasses import dataclass


@dataclass
class SimulationJob:
    unity_application_path: str
    project_path: str
    job_file_path: str
    # iteration_counter: str
    create_logs: bool = True

@dataclass
class SimulationRunResult:
    success: bool
    exit_code: int
    started_at: str
    finished_at: str

