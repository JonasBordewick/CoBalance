#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: parameter_settings_list_tile.py
Author: Jonas Bordewick
Date: 31.03.26
Contact: jonas.bordewick@uni-a.de
"""
import math
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QDoubleSpinBox, \
    QSpinBox, QSizePolicy

from app.domain.auto_suggestion import ParameterSettings
from app.models import ParameterTableRow


class ParameterSettingsListTile(QWidget):

    def __init__(self, entry: ParameterTableRow, parent=None):
        super().__init__(parent)
        self._entry = entry

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._build()
        self._set_values()

    def _build(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(8)

        header_layout = QHBoxLayout()

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        header_layout.addWidget(self.title_label)

        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_layout = QFormLayout()
        value_layout.setContentsMargins(10, 10, 10, 10)

        if self._entry.type == "float":
            self.min_spin = QDoubleSpinBox()
            self.min_spin.setDecimals(2)
            self.min_spin.setRange(-999999, 999999)
            self.min_spin.setSingleStep(0.01)

            self.max_spin = QDoubleSpinBox()
            self.max_spin.setDecimals(2)
            self.max_spin.setRange(-999999, 999999)
            self.min_spin.setSingleStep(0.01)

            self.step_spin = QDoubleSpinBox()
            self.step_spin.setDecimals(2)
            self.step_spin.setRange(0.01, 999999)
            self.min_spin.setSingleStep(0.01)
        else:
            self.min_spin = QSpinBox()
            self.min_spin.setRange(-999999, 999999)
            self.min_spin.setSingleStep(1)

            self.max_spin = QSpinBox()
            self.max_spin.setRange(-999999, 999999)
            self.min_spin.setSingleStep(1)

            self.step_spin = QSpinBox()
            self.step_spin.setRange(1, 999999)
            self.min_spin.setSingleStep(1)

        self.min_spin.setToolTip("Lower bound for this parameter. The algorithm will not generate values below this.")
        self.max_spin.setToolTip("Upper bound for this parameter. The algorithm will not generate values above this.")
        self.step_spin.setToolTip("Maximum change applied to this parameter per mutation. Smaller values produce finer adjustments; larger values explore the range more aggressively.")

        value_layout.addRow("Minimum", self.min_spin)
        value_layout.addRow("Maximum", self.max_spin)
        value_layout.addRow("Mutation Step", self.step_spin)

        root_layout.addLayout(header_layout)
        root_layout.addLayout(value_layout)

    def _set_values(self):
        self.title_label.setText(f"{self._entry.entity_name} -- {self._entry.display_name}")

        current_value = self._entry.value
        min_value = current_value * 0.75
        max_value = current_value * 1.25

        if self._entry.type == "float":
            self.min_spin.setValue(min_value)
            self.max_spin.setValue(max_value)
            self.step_spin.setValue(0.2 * (max_value - min_value))
        else:
            int_min = int(math.ceil(min_value))
            int_max = int(math.ceil(max_value))
            self.min_spin.setValue(int_min)
            self.max_spin.setValue(int_max)
            self.step_spin.setValue(max(1, round(0.2 * (int_max - int_min))))

    def get_settings(self) -> ParameterSettings:
        return ParameterSettings(
            parameter_key=self._entry.key,
            parameter_type=self._entry.type,
            value_min=self.min_spin.value(),
            value_max=self.max_spin.value(),
            mutation_step=self.step_spin.value(),
        )
