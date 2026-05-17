#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: json_serializer.py
Author: Jonas Bordewick
Date: 10.02.2026
Contact: jonas.bordewick@uni-a.de
"""
import os

from app.models import BalanceFile, AppSettings, ProjectSettings
from app.models.job_settings import JobSettings


class JsonSerializer:
    @staticmethod
    def load_balance_from_file(file_path: str):
        with open(file_path, 'r') as file:
            json_str = file.read()
            return BalanceFile.from_json(json_str)

    @staticmethod
    def save_balance_to_file(balance_dto: BalanceFile, file_path: str):
        json_str = balance_dto.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)

    @staticmethod
    def load_app_settings_from_file(file_path: str) -> AppSettings:
        try:
            with open(file_path, 'r') as file:
                json_str = file.read()
                return AppSettings.from_json(json_str)
        except FileNotFoundError:
            app_settings = AppSettings()
            JsonSerializer.save_app_settings_to_file(app_settings, file_path)
            return app_settings # Return default settings if file not found

    @staticmethod
    def save_app_settings_to_file(app_settings: AppSettings, file_path: str):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        json_str = app_settings.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)

    @staticmethod
    def load_project_settings_from_file(file_path: str) -> ProjectSettings:
        with open(file_path, 'r') as file:
            json_str = file.read()
            return ProjectSettings.from_json(json_str)

    @staticmethod
    def save_project_settings_to_file(project_settings: ProjectSettings, file_path: str):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        json_str = project_settings.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)

    @staticmethod
    def save_job_settings_to_file(job_settings: JobSettings, file_path: str):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        json_str = job_settings.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)