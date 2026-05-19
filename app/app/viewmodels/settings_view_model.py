#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: settings_view_model.py
Author: Jonas Bordewick
Date: 17.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import math
import os
import platform

from PyQt6.QtCore import QObject, pyqtSignal

from app.io import JsonSerializer
from app.io.repositories import ProjectSettingsRepository
from app.models import ProjectSettings, AppSettings
from .project_context_view_model import ProjectContextViewModel


class SettingsViewModel(QObject):
    """Manages app-wide and project-level settings, and persists them to disk.

    App settings (theme, defaults) are stored in a platform-specific user directory.
    Project settings are stored alongside the .cb file.
    """

    settings_changed = pyqtSignal()

    def __init__(
            self,
            project_context_view_model: ProjectContextViewModel,
    ):
        super().__init__()
        self._project_settings: ProjectSettings | None = None
        if platform.system() == "Windows":
            self._app_settings_path = os.path.join(
                os.environ['APPDATA'],
                "BalancingTool",
                "app_settings.json"
            )
        else:
            self._app_settings_path = os.path.join(
                os.environ['HOME'],
                ".BalancingTool",
                "app_settings.json"
            )
        self._app_settings = (JsonSerializer.
                             load_app_settings_from_file(self._app_settings_path))

        self._project_context_view_model = project_context_view_model
        self._project_context_view_model.project_changed.connect(
            self._on_open_project
        )

    @property
    def project_settings(self) -> ProjectSettings:
        return self._project_settings

    @property
    def app_settings(self) -> AppSettings:
        return self._app_settings

    @property
    def balances(self) -> dict[str, str]:
        return self._project_context_view_model.available_balances

    @property
    def scenes(self) -> dict[str, str]:
        return self._project_context_view_model.available_scenes

    def set_theme(self, theme: str):
        self._app_settings.theme = theme

    def set_auto_save(self, checked: bool):
        self._app_settings.auto_save = checked

    def set_default_number_of_runs(self, number_of_runs: int):
        self._app_settings.default_number_of_runs = number_of_runs

    def set_default_time_scale(self, time_scale: float):
        self._app_settings.default_time_scale = time_scale

    def set_default_max_simulation_time(self, max_simulation_time: int):
        self._app_settings.default_max_simulation_time = max_simulation_time

    def set_default_log_tick_rate(self, value: int):
        """Converts the user-visible seconds value to the internal fixed-timestep tick count."""
        if self._project_settings is None:
            return
        self._project_settings.default_log_tick_rate = math.floor(value / 0.02)

    def set_default_balance_file(self, text: str, save: bool = False):
        if self._project_settings is None:
            return
        self._project_settings.default_balance_file = text
        if save:
            self.save()


    def set_unity_application_path(self, text: str):
        if self._project_settings is None:
            return
        self._project_settings.unity_application_path = text

    def save(self):
        """Persists both app settings and project settings to their respective files."""
        JsonSerializer.save_app_settings_to_file(file_path=self._app_settings_path, app_settings=self.app_settings)
        if not self.project_settings:
            return
        JsonSerializer.save_project_settings_to_file(project_settings=self._project_settings, file_path=self.app_settings.last_opened_file)
        self._project_context_view_model.on_settings_save()
        self.settings_changed.emit()

    def _on_open_project(self):
        project_settings_path = self._project_context_view_model.current_project_path
        self._app_settings.last_opened_file = project_settings_path
        ProjectSettingsRepository.save_app_settings(
            app_settings=self.app_settings,
            file_path=self._app_settings_path
        )
        self._project_settings = self._project_context_view_model.current_project_settings

        self.settings_changed.emit()

    def get_default_balance_file_path(self) -> str:
        """Returns the absolute path to the default balance file, appending .json if needed."""
        if not self.app_settings.last_opened_file:
            return self.project_settings.default_balance_file
        base_dir = os.path.dirname(self.app_settings.last_opened_file)
        if self.project_settings.default_balance_file.endswith(".json"):
            return os.path.join(base_dir, "Balances", self.project_settings.default_balance_file)
        return os.path.join(base_dir, "Balances" ,self.project_settings.default_balance_file + ".json")