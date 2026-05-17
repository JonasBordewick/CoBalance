#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: project_settings.py
Author: Jonas Bordewick
Date: 04.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass


@dataclass
class ProjectSettings:
    version: str = "1.0"
    enable_time_based_logging: bool = True
    default_log_tick_rate: int = 50
    default_balance_file: str = "default_balance.json"
    unity_application_path: str = ""
    project_path: str = ""

    def set_version(self, version: str):
        self.version = version

    def set_default_log_tick_rate(self, tick_rate: int):
        self.default_log_tick_rate = tick_rate

    def set_default_balance_file(self, balance_file: str):
        self.default_balance_file = balance_file

    def set_unity_application_path(self, unity_application_path: str):
        self.unity_application_path = unity_application_path

    def set_project_path(self, project_path: str):
        self.project_path = project_path

    @staticmethod
    def from_json(json_str: str):
        import json
        data = json.loads(json_str)
        return ProjectSettings(
            version=data.get('version', '1.0'),
            enable_time_based_logging=data.get('enableTimeBasedLogging', True),
            default_log_tick_rate=data.get('defaultLogTickRate', 50),
            default_balance_file=data.get('defaultBalanceFile', 'default_balance.json'),
            unity_application_path=data.get('unityApplicationPath', ''),
            project_path=data.get('projectPath', '')
        )

    def to_json(self) -> str:
        import json
        return json.dumps({
            'version': self.version,
            'enableTimeBasedLogging': self.enable_time_based_logging,
            'defaultLogTickRate': self.default_log_tick_rate,
            'defaultBalanceFile': self.default_balance_file,
            'unityApplicationPath': self.unity_application_path,
            'projectPath': self.project_path
        }, indent=4)
