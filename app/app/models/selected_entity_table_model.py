#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: selected_entity_table_model.py
Author: Jonas Bordewick
Date: 22.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.models import BalanceFile, EntityDefinition
from app.models.selected_entity_table_row import SelectedEntityTableData
from app.viewmodels import BalanceViewModel, AppViewModel


@dataclass(frozen=True)
class CompareRow:
    param_key: str
    param_name: str

class SelectedEntityTableModel(QAbstractTableModel):
    """
    Columns:
      0 = "Paramter/Entity"
      1...n = selected entities
    Rows:
      0...m = Intersection of all parameters of all selected entities,
      sorted by display name
    """

    def __init__(self, balance_vm: BalanceViewModel, app_vm: AppViewModel):
        super().__init__()
        self._balance_vm = balance_vm
        self._app_vm = app_vm

        self._rows: list[CompareRow]

        self._entity_by_id = {}

        if balance_vm.file:
            self.set_balance()

    def set_balance(self):
        self.beginResetModel()
        self._entity_by_id = {e.key: e for e in self._balance_vm.file.entities}
        self._rebuild()
        self.endResetModel()

    def update_table_model(self):
        self.beginResetModel()
        self._rebuild()
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if not self._balance_vm.file:
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # 1 fixed + N entities
        return 1 + len(self._app_vm.comparison_entities)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Parameter/Entity"
            ent = self._app_vm.comparison_entities[section - 1]
            return ent.display_name

        return str(section + 1)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not self._balance_vm.file:
            return None

        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # first column: parameter name
            if col == 0:
                return row.param_name

            # entity columns: value for (entity, param)
            ent = self._app_vm.comparison_entities[col - 1]

            value = self._balance_vm.file.values.get(ent.key + "." +row.param_key, None)

            if value is None:
                return ""

            value_type = "float"
            for e in self._balance_vm.file.entities:
                if e.key == ent.key:
                    for p in e.parameters:
                        if p.key == ent.key + "." + row.param_key:
                            value_type = p.type
                            break
                    break

            return str(int(value)) if value_type == "int" else f"{float(value):g}"

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col == 0:
                return int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            return int(Qt.AlignmentFlag.AlignCenter)

        if role == Qt.ItemDataRole.EditRole:
            if col == 0:
                return ""
            if not self._balance_vm.file:
                return ""
            ent = self._app_vm.comparison_entities[col - 1]
            value = self._balance_vm.file.values.get(ent.key + "." +row.param_key, None)
            if value is None:
                return ""
            value_type = "float"
            for e in self._balance_vm.file.entities:
                if e.key == ent.key:
                    for p in e.parameters:
                        if p.key == ent.key + "." + row.param_key:
                            value_type = p.type
                            break
                    break

            return str(int(value)) if value_type == "int" else f"{float(value):g}"

        return None

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        col = index.column()

        if col == 0:
            return Qt.ItemFlag.ItemIsEnabled

        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role = ...):
        if role != Qt.ItemDataRole.EditRole:
            return False
        if not index.isValid():
            return False
        if index.column() == 0:
            return False
        if not self._balance_vm.file:
            return False

        row = self._rows[index.row()]
        ent = self._app_vm.comparison_entities[index.column() - 1]
        key = ent.key + "." + row.param_key

        # try to parse value as int or float
        try:
            if "." in value:
                parsed_value = float(value)
            else:
                parsed_value = int(value)
        except ValueError:
            return False

        self._balance_vm.set_value(key, parsed_value)
        return True

    def _rebuild(self):
        self._selected_entities = []
        self._rows = []

        if not self._balance_vm.file:
            return

        self._rows = [
            CompareRow(param_id, self._app_vm.param_name_lookup[param_id])
            for param_id in self._app_vm.common_parameters
        ]

        self._rows.sort(key=lambda r: r.param_name.lower())