#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_table_model.py
Author: Jonas Bordewick
Date: 08.03.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations

import datetime
import os
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel
from docopt import Optional

from .logs_table_row import LogsTableRow
from app.viewmodels import LogsExplorerViewModel
from ..utilities import normalize_group_name


class LogsTableModel(QAbstractTableModel):
    COL_FILE_NAME = 0
    COL_TIMESTAMP = 1
    COL_GROUP = 2

    Headers = ["File Name", "Timestamp", "Group"]

    def __init__(self, logs_explorer_view_model: LogsExplorerViewModel, rows: Optional[list[LogsTableRow]] = None):
        super().__init__()
        self._rows: list[LogsTableRow] = rows or []
        self._logs_explorer_view_model = logs_explorer_view_model
        self._logs_group_view_model = logs_explorer_view_model.logs_group_view_model

    def set_rows(self, rows: list[LogsTableRow]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()


    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.Headers)

    def headerData(self, section, orientation, role = ...):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.Headers[section]
        return str(section + 1)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.COL_FILE_NAME:
                return os.path.splitext(row.file_name)[0]
            if col == self.COL_TIMESTAMP:
                return datetime.datetime.fromtimestamp(row.timestamp).strftime('%H:%M:%S %d.%m.%Y')
            if col == self.COL_GROUP:
                group = self._logs_group_view_model.get_group_for_log(row.file_name)
                if group:
                    return group.name
                return ""
        if role == Qt.ItemDataRole.UserRole:
            # UserRole returns raw, sortable values used by LogsTableProxyModel.
            # The timestamp column must return a float here so the proxy sorts
            # chronologically instead of lexicographically on the formatted string.
            if col == self.COL_TIMESTAMP:
                return row.timestamp
            if col == self.COL_FILE_NAME:
                return os.path.splitext(row.file_name)[0].lower()
            if col == self.COL_GROUP:
                group = self._logs_group_view_model.get_group_for_log(row.file_name)
                return group.name.lower() if group else ""
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)
        if role == Qt.ItemDataRole.EditRole:
            if col == self.COL_GROUP:
                group = self._logs_group_view_model.get_group_for_log(row.file_name)
                if group:
                    return group.name
                return ""
        return None

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        base = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        if index.column() == self.COL_GROUP:
            return base | Qt.ItemFlag.ItemIsEditable
        return base

    def setData(self, index, value, role = ...):
        if role != Qt.ItemDataRole.EditRole:
            return False
        if index.column() != self.COL_GROUP:
            return False
        row = self._rows[index.row()]
        new_name = str(value).strip()

        current_group = self._logs_group_view_model.get_group_for_log(row.file_name)

        if not new_name:
            if current_group is None:
                return False
            self._logs_group_view_model.remove_logs_from_group([row.file_name])
            return True

        existing_group = self._logs_group_view_model.find_group_by_name(new_name)

        if current_group is not None:
            same_group = (
                    normalize_group_name(current_group.name)
                    == normalize_group_name(new_name)
            )
            if same_group:
                return False

        if existing_group is not None:
            self._logs_group_view_model.assign_logs_to_group_by_name([row.file_name], existing_group.name)
            return True

        self._logs_group_view_model.create_group_from_logs([row.file_name], new_name)
        return True

    def row_at(self, at: int) -> Optional[LogsTableRow]:
        if at < 0 or at >= len(self._rows):
            return None
        return self._rows[at]

class LogsTableProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # Use UserRole for sorting so the timestamp column compares raw float
        # values instead of the human-readable string returned by DisplayRole.
        self.setSortRole(Qt.ItemDataRole.UserRole)

    def filterAcceptsRow(self, source_row, source_parent):
        pattern = self.filterRegularExpression().pattern()
        if not pattern:
            return True
        model = self.sourceModel()
        for col in range(model.columnCount()):
            index = model.index(source_row, col, source_parent)
            data = model.data(index, Qt.ItemDataRole.DisplayRole)
            if data and pattern in str(data):
                return True
        return False