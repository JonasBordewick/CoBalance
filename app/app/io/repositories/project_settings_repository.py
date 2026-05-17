#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: project_settings_repository.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import os.path

from app.models import ProjectSettings, AppSettings


class ProjectSettingsRepository:

    @staticmethod
    def load_project_settings(file_path: str) -> ProjectSettings:
        try:
            with open(file_path, 'r') as file:
                json_str = file.read()
                return ProjectSettings.from_json(json_str)
        except FileNotFoundError:
            project_settings = ProjectSettings()
            ProjectSettingsRepository.save_project_settings(file_path, project_settings)
            return project_settings # Return default settings if file not found

    @staticmethod
    def save_project_settings(file_path: str, project_settings: ProjectSettings):
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(project_settings.to_json())

    @staticmethod
    def load_app_settings(file_path: str) -> AppSettings:
        try:
            with open(file_path, 'r') as file:
                json_str = file.read()
                return AppSettings.from_json(json_str)
        except FileNotFoundError:
            app_settings = AppSettings()
            ProjectSettingsRepository.save_app_settings(file_path, app_settings)
            return app_settings

    @staticmethod
    def save_app_settings(file_path: str, app_settings: AppSettings):
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(app_settings.to_json())

