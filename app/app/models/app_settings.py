#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: app_settings.py
Author: Jonas Bordewick
Date: 13.02.2026
Contact: jonas.bordewick@uni-a.de
"""

import json
from dataclasses import dataclass

@dataclass
class AppSettings:
    theme: str = 'light'
    last_opened_file: str = ''
    auto_save: bool = False
    default_number_of_runs: int = 1
    default_time_scale: float = 5.0
    default_max_simulation_time: int = 300
    # Genetic Algorithm Settings
    defautl_generation_size = 0

    def set_theme(self, theme: str):
        self.theme = theme

    def set_last_opened_file(self, file_path: str):
        self.last_opened_file = file_path

    def set_auto_save(self, auto_save: bool):
        self.auto_save = auto_save

    def set_default_number_of_runs(self, number_of_runs: int):
        self.default_number_of_runs = number_of_runs

    def set_default_time_scale(self, time_scale: float):
        self.default_time_scale = time_scale

    def set_default_max_simulation_time(self, max_simulation_time: int):
        self.default_max_simulation_time = max_simulation_time

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        return AppSettings(
            theme=data.get('theme', 'light'),
            last_opened_file=data.get('last_opened_file', ''),
            auto_save=data.get('auto_save', False),
            default_number_of_runs=data.get('default_number_of_runs', 1),
            default_time_scale=data.get('default_time_scale', 5.0),
            default_max_simulation_time=data.get('default_max_simulation_time', 300)
        )

    def to_json(self) -> str:
        return json.dumps({
            'theme': self.theme,
            'last_opened_file': self.last_opened_file,
            'auto_save': self.auto_save,
            'default_number_of_runs': self.default_number_of_runs,
            'default_time_scale': self.default_time_scale,
            'default_max_simulation_time': self.default_max_simulation_time
        }, indent=4)