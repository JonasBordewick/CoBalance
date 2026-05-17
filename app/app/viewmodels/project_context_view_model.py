#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: project_context_view_model.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import os

from PyQt6.QtCore import QObject, pyqtSignal

from app.enums import ScreenType
from app.io.repositories import ProjectSettingsRepository
from app.io.watchers import DirectoryWatcherService
from app.models import ProjectSettings

class ProjectContextViewModel(QObject):
    """Central context for an open project: paths, available assets, current screen, and errors.

    Acts as the single source of truth for which project is open. Other ViewModels
    subscribe to project_changed to initialise themselves whenever a new project is loaded.
    """

    file_watcher_key_balances = "Balances"
    file_watcher_key_scenes = "Scenes"

    project_changed = pyqtSignal()
    screen_changed = pyqtSignal(int)
    available_scenes_changed = pyqtSignal()
    available_balances_changed = pyqtSignal()

    error_changed = pyqtSignal()

    def __init__(
            self,
            file_watcher: DirectoryWatcherService
    ):
        super().__init__()

        self._current_project_path: str | None = None
        self._current_project_directory: str | None = None
        self._current_project_settings: ProjectSettings | None = None
        self._current_screen: ScreenType = ScreenType.PARAMETERS
        self._available_scenes: dict[str, str] = dict()
        self._available_balances: dict[str, str] = dict()
        self._current_balance_path: str | None = None
        self._current_balance: str | None = None
        self._logs_directory: str | None = None
        self._jobs_directory: str | None = None
        self._balance_directory: str | None = None
        self._scenes_directory: str | None = None

        self._progess_file_path: str | None = None

        self._error_log: list[str] = []

        self._watcher = file_watcher
        self._watcher.watched_directory_changed.connect(self._on_directory_changed)

    # Properties

    @property
    def current_project_path(self) -> str | None:
        return self._current_project_path
    @property
    def current_project_directory(self) -> str | None:
        return self._current_project_directory
    @property
    def current_balance_path(self) -> str | None:
        return self._current_balance_path
    @property
    def current_project_settings(self) -> ProjectSettings | None:
        return self._current_project_settings
    @property
    def current_screen(self) -> ScreenType:
        return self._current_screen
    @property
    def current_balance(self) -> str | None:
        return self._current_balance
    @property
    def available_scenes(self) -> dict[str, str]:
        return self._available_scenes
    @property
    def available_balances(self) -> dict[str, str]:
        return self._available_balances
    @property
    def logs_directory(self) -> str | None:
        return self._logs_directory
    @property
    def jobs_directory(self) -> str | None:
        return self._jobs_directory
    @property
    def balances_directory(self) -> str | None:
        return self._balance_directory
    @property
    def scenes_directory(self) -> str | None:
        return self._scenes_directory
    @property
    def current_project_name(self) -> str | None:
        if not self._current_project_settings:
            return None
        return self._current_project_settings.project_path.split(os.sep)[-1]

    @property
    def progress_file_path(self) -> str | None:
        return self._progess_file_path

    @property
    def error_log(self) -> list[str]:
        return self._error_log

    @property
    def latest_error(self) -> str | None:
        if not self._error_log:
            return None
        return self._error_log[-1]

    def on_error(self, error_message: str):
        """Appends an error to the log and notifies listeners."""
        self._error_log.append(error_message)
        self.error_changed.emit()


    def open_project(self, project_file_path: str) -> None:
        """Loads a project file and sets up all derived paths and filesystem watchers."""
        self._current_project_path = project_file_path
        self._current_project_directory = os.path.dirname(self._current_project_path)
        self._current_project_settings = ProjectSettingsRepository.load_project_settings(project_file_path)
        self._progess_file_path = os.path.join(self._current_project_directory, ".progress.json")
        self._current_screen = ScreenType.PARAMETERS
        self._available_scenes = dict()
        self._available_balances = dict()

        self._balance_directory = os.path.join(self._current_project_directory, "Balances")
        self._logs_directory = os.path.join(self._current_project_directory, "Logs")
        self._jobs_directory = os.path.join(self._current_project_directory, "Jobs")
        self._scenes_directory = os.path.join(
            self._current_project_settings.project_path,
            "Assets",
            "Scenes",
        )

        self._load_balances(emit=False)
        self._load_scenes(emit=False)

        if self._current_project_settings.default_balance_file.endswith(".json"):
            self._current_project_settings.default_balance_file =  self._current_project_settings.default_balance_file[:-5]


        self._current_balance = self._current_project_settings.default_balance_file
        self._current_balance_path = self._available_balances.get(self._current_balance)

        self._watcher.watch_directory(
            directory_key=self.file_watcher_key_scenes,
            directory_path=self._scenes_directory,
        )
        self._watcher.watch_directory(
            directory_key=self.file_watcher_key_balances,
            directory_path=self._balance_directory,
        )

        self.project_changed.emit()

    def set_screen(self, screen: ScreenType):
        if self._current_screen == screen:
            return
        self._current_screen = screen
        self.screen_changed.emit(screen)

    def on_settings_save(self):
        self._current_balance = self._current_project_settings.default_balance_file
        self._current_balance_path = self._available_balances.get(self._current_balance)

    def _on_directory_changed(self, directory_key: str, _: str, initial_load: bool):
        if directory_key == self.file_watcher_key_balances:
            self._load_balances(emit=True)
        elif directory_key == self.file_watcher_key_scenes:
            self._load_scenes(emit=True)

    def _load_balances(self, emit: bool):
        if not self._current_project_settings:
            return

        self._available_balances = {}

        for file_name in os.listdir(self._balance_directory):
            if file_name.endswith(".json"):
                self._available_balances[os.path.splitext(file_name)[0]] = os.path.join(self._balance_directory, file_name)

        if emit:
            self.available_balances_changed.emit()

    def _load_scenes(self, emit: bool):
        if not self._current_project_settings:
            return

        self._available_scenes = {}
        for root, dirs, files in os.walk(self._scenes_directory):
            for file_name in files:
                if file_name.endswith(".unity"):
                    scene_name = os.path.splitext(file_name)[0]
                    full_path = os.path.join(root, file_name)
                    self._available_scenes[scene_name] = full_path
        if emit:
            self.available_scenes_changed.emit()
