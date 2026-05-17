#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: group_manager.py
Author: Jonas Bordewick
Date: 14.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import os
from dataclasses import dataclass

from app.models import Group

import json

from app.utilities import normalize_group_name


class GroupManager:
    """Manages log groups and their persistence to a groups.json file.

    Groups are identified by an auto-incrementing string ID. Each log file
    can belong to at most one group. The state is serialised to JSON alongside
    the log directory so groups persist across sessions.
    """

    def __init__(self):
        self._groups_by_id: dict[str, Group] = {}
        self._group_id_by_log_name: dict[str, str] = {}
        self._next_group_id: int = 0

        self.file_path: str | None = None
        self.load_from_json()

    @property
    def groups_by_id(self) -> dict[str, Group]:
        return self._groups_by_id
    @property
    def group_id_by_log_name(self) -> dict[str, str]:
        return self._group_id_by_log_name

    # -------------------------
    # Setter
    # -------------------------

    def set_file_path(self, file_path: str) -> None:
        """Sets the groups.json path to the given directory and reloads from disk."""
        self.file_path = os.path.join(file_path, 'groups.json')
        self.load_from_json()

    # -------------------------
    # Utility Functions
    # -------------------------

    def remove_empty_groups(self) -> set[str]:
        """Deletes groups that have no log files assigned and returns their IDs."""
        used_group_ids = set(self.group_id_by_log_name.values())
        empty_group_ids = set(self.groups_by_id.keys()) - used_group_ids

        for group_id in empty_group_ids:
            self.groups_by_id.pop(group_id, None)

        return empty_group_ids

    # -------------------------
    # Query Functions
    # -------------------------

    def find_group_by_name(self, name: str) -> Group | None:
        """Looks up a group by name using normalised comparison (case-insensitive)."""
        normalized_name = normalize_group_name(name)
        for group in self.groups_by_id.values():
            if normalize_group_name(group.name) == normalized_name:
                return group
        return None

    def get_group_for_log(self, log_name: str) -> Group | None:
        group_id = self.group_id_by_log_name.get(log_name)
        if group_id is None:
            return None
        return self.groups_by_id.get(group_id)

    # -------------------------
    # Group Operations
    # -------------------------
    def create_group_from_logs(self, log_names: list[str], name: str | None = None):
        """Creates a new group containing the given logs.

        If no name is provided the group ID is used as a fallback name.
        Raises ValueError if the log list is empty or the name is already taken.
        """
        if not log_names:
            raise ValueError("Cannot create group from empty log list")

        group_id = f"group_{self._next_group_id}"
        self._next_group_id += 1

        if name is None or not name.strip():
            name = group_id

        name = name.strip()
        if not name:
            raise ValueError("Group name cannot be empty")

        if self.find_group_by_name(name) is not None:
            raise ValueError(f"Group with name '{name}' already exists")

        group = Group(id=group_id, name=name)
        self.groups_by_id[group_id] = group

        for log_name in log_names:
            self.group_id_by_log_name[log_name] = group_id

    def rename_group(self, group_id: str, new_name: str):
        """Renames a group, rejecting duplicates and no-op renames (normalised comparison)."""
        group = self.groups_by_id.get(group_id)
        if group is None:
            raise ValueError(f"Group with id {group_id} does not exist")
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("Group name cannot be empty")

        if normalize_group_name(group.name) == normalize_group_name(new_name):
            return

        if self.find_group_by_name(new_name) is not None:
            raise ValueError(f"Group with name '{new_name}' already exists")

        group.name = new_name

    def delete_group(self, group_id: str):
        """Deletes a group and unassigns all logs that belonged to it."""
        if group_id not in self.groups_by_id:
            raise ValueError(f"Group with id {group_id} does not exist")
        self.groups_by_id.pop(group_id)

        # Remove all logs from this group
        logs_to_remove = [log_name for log_name, g_id in self.group_id_by_log_name.items() if g_id == group_id]
        for log_name in logs_to_remove:
            self.group_id_by_log_name.pop(log_name, None)


    def remove_logs_from_group(self, log_names: list[str]):
        """Unassigns the given logs from their group and removes any groups that become empty."""
        for log_name in log_names:
            self.group_id_by_log_name.pop(log_name, None)
        self.remove_empty_groups()

    def assign_logs_to_group_by_name(self, log_names: list[str], group_name: str):
        """Moves the given logs into an existing group, overwriting any previous assignment."""
        group = self.find_group_by_name(group_name)
        if group is None:
            raise ValueError(f"Group with name '{group_name}' does not exist")

        for log_name in log_names:
            self.group_id_by_log_name[log_name] = group.id



    # -------------------------
    # JSON IO
    # -------------------------

    def load_from_json(self):
        if not self.file_path:
            return
        try:
            with open(self.file_path, 'r') as file:
                self.from_json(file.read())
        except FileNotFoundError:
            self._groups_by_id = {}
            self._group_id_by_log_name = {}
            self._next_group_id = 0
            self.save_to_json()

    def save_to_json(self):
        """Writes the current group state to groups.json, pruning empty groups first."""
        if not self.file_path:
            return
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.remove_empty_groups()
        with open(self.file_path, 'w') as file:
            file.write(self.to_json())

    def from_json(self, json_str: str):
        data = json.loads(json_str)
        self._groups_by_id = {
            group['id']: Group.from_dict(group)
            for group in data.get('groups', [])
        }
        self._group_id_by_log_name = data.get('logToGroup', {})
        self._next_group_id = data.get('nextGroupId', 0)

    def to_json(self) -> str:
        return json.dumps({
            "groups": [group.to_dict() for group in self._groups_by_id.values()],
            "logToGroup": self._group_id_by_log_name,
            "nextGroupId": self._next_group_id
        }, indent=4)
