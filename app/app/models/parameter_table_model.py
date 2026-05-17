#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: parameter_table_model.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations
from typing import Any, Optional
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel

from .entity_table_row import EntityTableRow
from .parameter_table_row import ParameterTableRow
from ..viewmodels import BalanceViewModel


class ParameterTableModel(QAbstractTableModel):
    COL_PARAMETER = 0
    COL_VALUE = 1
    COL_ENTITY = 2
    COL_CATEGORY = 3
    COL_TAGS = 4

    Headers = ["Parameter Name", "Value", "Entity", "Category", "Tags"]

    def __init__(self, vm: BalanceViewModel, rows: Optional[list[ParameterTableRow]] = None):
        super().__init__()
        self._rows: list[ParameterTableRow] = rows or []
        self._vm = vm

    def set_rows(self, rows: list[ParameterTableRow]):
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
            if col == self.COL_PARAMETER:
                return row.display_name
            if col == self.COL_VALUE:
                if not self._vm.file:
                        return ""
                val = self._vm.file.values.get(row.key, None)
                if val is None:
                    return ""
                return str(int(val)) if row.type == "int" else f"{float(val):g}"
            if col == self.COL_ENTITY:
                return row.entity_name
            if col == self.COL_CATEGORY:
                return row.category
            if col == self.COL_TAGS:
                if not self._vm.file:
                    return ""
                tags = self._vm.get_tags(row.entity_id, row.key)
                return ", ".join(tags)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)

        if role == Qt.ItemDataRole.EditRole:
            if col == self.COL_VALUE:
                if not self._vm.file:
                    return ""
                val = self._vm.file.values.get(row.key, None)
                if val is None:
                    return ""
                return str(int(val)) if row.type == "int" else f"{float(val):g}"
            if col == self.COL_TAGS:
                if not self._vm.file:
                    return ""
                tags = self._vm.get_tags(row.entity_id, row.key)
                return ", ".join(tags)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        base =  Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        if index.column() == self.COL_VALUE or index.column() == self.COL_TAGS:
            return base | Qt.ItemFlag.ItemIsEditable
        return base

    def setData(self, index, value, role = ...):
        if role != Qt.ItemDataRole.EditRole:
            return False
        if not index.isValid():
            return False
        if not (index.column() == self.COL_VALUE or index.column() == self.COL_TAGS):
            return False
        if not self._vm.file:
            return False

        row = self._rows[index.row()]

        if index.column() == self.COL_VALUE:
            try:
                casted = int(value) if row.type == "int" else float(value)
            except Exception as e:
                return False

            self._vm.set_value(row.key, casted)

        if index.column() == self.COL_TAGS:
            tags = [t.strip() for t in value.split(",")]
            self._vm.set_tags(row.entity_id, row.key, tags)

        idx = self.index(index.row(), index.column())
        self.dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        return True

    def row_at(self, at: int) -> Optional[ParameterTableRow]:
        if at <0 or at >= len(self._rows):
            return None
        return self._rows[at]

class ParameterTableFilterProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def filterAcceptsRow(self, source_row, source_parent):
        pattern = self.filterRegularExpression().pattern()
        if not pattern:
            return True

        model = self.sourceModel()
        for col in range(model.columnCount()):
            index = model.index(source_row, col, source_parent)
            text = model.data(index, Qt.ItemDataRole.DisplayRole)
            if text is None:
                continue
            if pattern.lower() in str(text).lower():
                return True
        return False
