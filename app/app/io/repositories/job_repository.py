#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: job_repository.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import os

from app.models.job_settings import JobSettings


class JobRepository:

    @staticmethod
    def save_job_settings_to_file(job_settings: JobSettings, file_path: str):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        json_str = job_settings.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)