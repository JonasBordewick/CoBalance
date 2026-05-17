#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: balance_view_model.py
Author: Jonas Bordewick
Date: 10.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional
import os

from app.io.repositories import BalanceRepository
from app.io.watchers import DirectoryWatcherService
from app.models import BalanceFile
from .project_context_view_model import ProjectContextViewModel


class BalanceViewModel(QObject):
    """Manages loading, saving, and tracking changes to the active balance file.

    Watches the file on disk for external edits and notifies the UI whether the
    in-memory state has unsaved changes (dirty flag).
    """

    file_loaded = pyqtSignal()
    file_path_changed = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    load_state_changed = pyqtSignal(bool)
    dirty_changed = pyqtSignal(bool)
    balance_file_changed = pyqtSignal()

    external_file_changed = pyqtSignal()

    file_watcher_key = "BalanceFile"

    def __init__(
            self,
            file_watcher: DirectoryWatcherService,
            project_context_view_model: ProjectContextViewModel
    ):
        super().__init__()
        self._file: Optional[BalanceFile] = None
        self._path: str = ""
        self._dirty = False

        self.watcher = file_watcher
        self.watcher.watched_file_changed.connect(self._on_watched_file_changed)

        self.project_context_view_model = project_context_view_model
        self.project_context_view_model.project_changed.connect(
            self._on_open_project
        )

    @property
    def file(self) -> Optional[BalanceFile]:
        return self._file

    @property
    def path(self) -> str:
        return self._path

    @property
    def is_loaded(self) -> bool:
        return self._file is not None

    @property
    def is_dirty(self) -> bool:
        return self._dirty

    def _set_dirty(self, dirty: bool, emit: bool = True):
        if self._dirty == dirty:
            return
        self._dirty = dirty
        if emit:
            self.dirty_changed.emit(dirty)


    def _on_open_project(self):
        """Loads the default balance file when a project is opened."""
        try:
            current_path = self.project_context_view_model.current_balance_path
            bf = BalanceRepository.load_balance_from_file(current_path)

            self._file = bf

            self._set_dirty(False)
            self.watcher.watch_file(self.file_watcher_key, self._path)

            self.file_path_changed.emit(current_path)
            self.status_changed.emit("File loaded successfully.")
            self.file_loaded.emit()
            self.load_state_changed.emit(True)
            return True
        except Exception as e:
            self.project_context_view_model.on_error(str(e))
            self.status_changed.emit("Failed to load file.")
            print("Failed to load file.")
            self.load_state_changed.emit(False)
            return False

    def reload_from_path(self) -> bool:
        """Reloads the current balance file from disk, discarding in-memory changes."""
        try:
            current_path = self.project_context_view_model.current_balance_path
            bf = BalanceRepository.load_balance_from_file(current_path)

            self._file = bf
            self._path = current_path

            self._set_dirty(False)
            self.watcher.watch_file(self.file_watcher_key, self._path)

            self.file_path_changed.emit(current_path)
            self.status_changed.emit("File loaded successfully.")
            self.file_loaded.emit()
            self.load_state_changed.emit(True)
            return True
        except Exception as e:
            self.project_context_view_model.on_error(str(e))
            self.status_changed.emit("Failed to load file.")
            print("Failed to load file.")
            self.load_state_changed.emit(False)
            return False

    def _on_watched_file_changed(self, key: str, path: str, is_initial: bool):
        """Reacts to a filesystem change on the watched balance file.

        If the file changed externally and the user has unsaved edits, a signal
        is emitted so the UI can ask whether to discard those changes. On the
        initial watch registration (is_initial=True) the reload is silent.
        """
        if key != self.file_watcher_key:
            return

        if not os.path.exists(path):
            return

        if self.is_dirty:
            if not is_initial:
                self.status_changed.emit(
                    "File changed on disk, but you have unsaved changes."
                )
                self.external_file_changed.emit()
            return

        try:
            bf = BalanceRepository.load_balance_from_file(path)

            if not self._file.has_diff(bf): return

            self._file = bf

            self._set_dirty(False, emit=not is_initial)

            if not is_initial:
                self.status_changed.emit("File reloaded (external change detected).")
                self.file_loaded.emit()
                self.balance_file_changed.emit()

        except Exception as e:
            if not is_initial:
                self.status_changed.emit(f"Failed to reload changed file. {str(e)}")

    def save_to_path(self, path: str, emit: bool = True):
        """Saves the current balance file to the given path and clears the dirty flag."""
        if not self._file:
            return
        try:
            BalanceRepository.save_balance_to_file(self._file, path)

            self._path = path
            self._set_dirty(False, emit)
            self.watcher.watch_file(self.file_watcher_key, self._path)

            self.status_changed.emit("File saved successfully.")
            self.file_path_changed.emit(path)
        except Exception as e:
            self.project_context_view_model.on_error(str(e))
            self.status_changed.emit("Failed to save file.")

    def set_value(self, key: str, value) -> None:
        """Updates a single parameter value in memory and marks the file as dirty."""
        if not self._file:
            return
        old = self._file.values.get(key, None)
        if old == value:
            return
        self._file.values[key] = value
        self._set_dirty(True)
        self.balance_file_changed.emit()

    def set_tags(self, entity_id: str, param_key: str, value: list[str]) -> None:
        if not self._file:
            return

        entity = next((e for e in self._file.entities if e.key == entity_id), None)
        if not entity:
            return

        param = next((p for p in entity.parameters if p.key == param_key), None)
        if not param:
            return

        old = param.tags
        if old == value:
            return
        param.tags = value
        self._set_dirty(True)
        self.balance_file_changed.emit()

    def get_tags(self, entity_id: str, param_key: str) -> list[str]:
        if not self._file:
            return []

        entity = next((e for e in self._file.entities if e.key == entity_id), None)
        if not entity:
            return []

        param = next((p for p in entity.parameters if p.key == param_key), None)
        if not param:
            return []

        return param.tags