#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: auto_suggestion_models.py
Author: Jonas Bordewick
Date: 01.04.26
Contact: jonas.bordewick@uni-a.de
"""

from dataclasses import dataclass
from typing import Literal

ParamType = Literal["int", "float"]

@dataclass
class AutoSuggestionSettings:
    snapshot_id: str
    population_size: int
    generation_count: int
    elite_count: int
    runs_per_individual: int
    scene_path: str
    base_balance_file_path: str
    time_scale: float
    max_time: int
    parameter_settings: list['ParameterSettings']

@dataclass
class ParameterSettings:
    parameter_key: str
    parameter_type: ParamType
    value_min: float
    value_max: float
    mutation_step: float

@dataclass
class Candidate:
    id: str
    genes: dict[str, float]
    fitness: float | None = None
    result_path: str | None = None