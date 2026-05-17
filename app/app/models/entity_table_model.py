#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: entity_table_model.py
Author: Jonas Bordewick
Date: 21.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations
from typing import Any, Optional
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel

from .entity_table_row import EntityTableRow
from ..viewmodels import BalanceViewModel

class EntityTableModel(QAbstractTableModel):
    COL_NAME = 0
    COL_CATEGORY = 1

    Headers = ["Name", "Category"]

    def __init__(self, vm: BalanceViewModel, rows: Optional[list[EntityTableRow]] = None):
        super().__init__()
        self._rows: list[EntityTableRow] = rows or []
        self._vm = vm

    def set_rows(self, rows: list[EntityTableRow]):
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
            if col == self.COL_NAME:
                return row.display_name
            if col == self.COL_CATEGORY:
                return row.category
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)
        return None

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def row_at(self, at: int) -> Optional[EntityTableRow]:
        if at < 0 or at >= len(self._rows):
            return None
        return self._rows[at]

class EntityTableProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

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