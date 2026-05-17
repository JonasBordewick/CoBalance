#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_group_view_model.py
Author: Jonas Bordewick
Date: 23.03.26
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import QObject, pyqtSignal

from app.io import GroupManager
from app.models import Group


class LogsGroupViewModel(QObject):
    """Thin ViewModel layer over GroupManager that tracks unsaved changes and emits Qt signals.

    All mutation methods set the dirty flag and emit dirty_changed so the main
    window can enable the Save button and auto-save logic can react.
    """

    dirty_changed = pyqtSignal(bool)
    groups_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.group_manager = GroupManager()
        self._dirty = False

    @property
    def is_dirty(self) -> bool:
        return self._dirty

    @property
    def groups_by_id(self) -> dict[str, Group]:
        return self.group_manager.groups_by_id

    @property
    def group_id_by_log_name(self) -> dict[str, str]:
        return self.group_manager.group_id_by_log_name

    def get_selected_group_ids(self, selected_logs_names: set[str]) -> set[str]:
        group_ids = set()
        for log_name in selected_logs_names:
            group_id = self.group_id_by_log_name.get(log_name)
            if group_id is not None:
                group_ids.add(group_id)
        return group_ids

    def has_ungrouped_selected_logs(self, selected_logs_names: set[str]) -> bool:
        for log_name in selected_logs_names:
            if log_name not in self.group_id_by_log_name:
                return True
        return False

    def get_selected_groups(self, selected_logs_names: set[str]) -> list[Group]:
        """Returns the distinct groups that contain any of the selected logs, sorted by name."""
        group_ids = self.get_selected_group_ids(selected_logs_names)
        groups = [self.groups_by_id[group_id] for group_id in group_ids if group_id in self.groups_by_id]
        groups.sort(key=lambda g: g.name.casefold())
        return groups
    
    def set_file_path(self, path):
        self.group_manager.set_file_path(path)

    # -----------------------------------------------------------------------------------------------
    # --------------------------------------------GROUPS---------------------------------------------
    # -----------------------------------------------------------------------------------------------
    
    def save_to_file(self, emit: bool = True):
        self.group_manager.save_to_json()
        self._dirty = False
        if emit:
            self.dirty_changed.emit(False)

    def create_group_from_logs(self, log_names: list[str], name: str | None = None):
        self.group_manager.create_group_from_logs(log_names, name)
        self.groups_changed.emit()
        self._dirty = True
        self.dirty_changed.emit(True)

    def get_group_for_log(self, log_name: str) -> Group | None:
        return self.group_manager.get_group_for_log(log_name)

    def rename_group(self, group_id: str, new_name: str):
        self.group_manager.rename_group(group_id, new_name)
        self.groups_changed.emit()
        self._dirty = True
        self.dirty_changed.emit(True)

    def delete_group(self, group_id: str):
        self.group_manager.delete_group(group_id)
        self.groups_changed.emit()
        self._dirty = True
        self.dirty_changed.emit(True)

    def remove_logs_from_group(self, log_names: list[str]):
        self.group_manager.remove_logs_from_group(log_names)
        self._dirty = True
        self.dirty_changed.emit(True)

    def find_group_by_name(self, name: str) -> Group | None:
        return self.group_manager.find_group_by_name(name)

    def remove_empty_groups(self):
        empty_group_ids = self.group_manager.remove_empty_groups()
        if empty_group_ids:
            self.groups_changed.emit()
            self._dirty = True
            self.dirty_changed.emit(True)

    def assign_logs_to_group_by_name(self, log_names: list[str], group_name: str):
        self.group_manager.assign_logs_to_group_by_name(log_names, group_name)
        self.groups_changed.emit()
        self._dirty = True
        self.dirty_changed.emit(True)