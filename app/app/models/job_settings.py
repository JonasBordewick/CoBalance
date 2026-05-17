#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: job_settings.py
Author: Jonas Bordewick
Date: 21.03.2026
Contact: jonas.bordewick@uni-a.de
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class JobSettings:
    version: str = "1.0"
    job_id: str = "default"
    job_type: str = "simulation"
    input_settings: dict[str, Any] = field(default_factory=dict)
    execution_settings: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_json(json_str: str):
        import json
        data = json.loads(json_str)
        return JobSettings(
            version=data["version"],
            job_id=data["jobId"],
            job_type=data["jobType"],
            input_settings=data["input"],
            execution_settings=data["execution"]
        )

    def to_json(self) -> str:
        import json
        return json.dumps( {
            'version': self.version,
            'jobId': self.job_id,
            'jobType': self.job_type,
            'input': self.input_settings,
            'execution': self.execution_settings
        }, indent=4)