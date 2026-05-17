#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: app_view_model.py
Author: Jonas Bordewick
Date: 12.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from app.models import EntityDefinition, ProjectSettings, BalanceFile
from .project_context_view_model import ProjectContextViewModel

from ..enums import ComparisonChartType

@dataclass(frozen=True)
class ChartData:
    name: str
    values: list[float]
    raw_values: list[float]

class AppViewModel(QObject):
    """Manages the entity comparison chart: selected entities, common parameters, and chart data.

    Computes the intersection of parameters across selected entities and normalises
    each parameter column so all series are on a [0, 1] scale for visual comparison.
    """

    comparison_entity_selection_changed = pyqtSignal()
    comparison_chart_type_changed = pyqtSignal(int)

    def __init__(
            self,
            project_context_view_model: ProjectContextViewModel,
    ):
        super().__init__()
        self._project_context_view_model = project_context_view_model

        self.comparison_entities_ids: list[str] = []
        self.comparison_entities: list[EntityDefinition] = []

        self.common_parameters: set[str] = set()
        self.param_name_lookup: dict[str, str] = {}

        self.categories: list[str] = []
        self.chart_data: list[ChartData] = []

        self.comparison_chart_type = ComparisonChartType.BAR

        self.current_balance_file: BalanceFile | None = None

        self._entity_by_id = {}

    @property
    def selected_comparison_entities(self) -> list[str]:
        return self.comparison_entities_ids

    @property
    def chart_type(self) -> ComparisonChartType:
        return self.comparison_chart_type

    def set_comparison_chart_type(self, chart_type: ComparisonChartType):
        if self.comparison_chart_type == chart_type:
            return
        self.comparison_chart_type = chart_type
        self.comparison_chart_type_changed.emit(chart_type)

    def load_balance(self, balance: BalanceFile | None = None):
        if not balance:
            return

        self.current_balance_file = balance

        self._entity_by_id = {e.key: e for e in balance.entities}
        self.common_parameters: set[str] = set()
        self.param_name_lookup = {}

    def set_selected_comparison_entities(self, entities: list[str]):
        self.comparison_entities_ids = entities
        self.categories = []
        self.chart_data = []

        self.common_parameters: set[str] = set()
        self.param_name_lookup = {}

        if not self._entity_by_id:
            return

        self.comparison_entities = [
            self._entity_by_id[eid] for eid in self.comparison_entities_ids
            if eid in self._entity_by_id
        ]

        if not self.comparison_entities:
            self.comparison_entity_selection_changed.emit()
            return


        self.set_common_parameters()
        self.reload_chart_data()

    def set_common_parameters(self):
        """Computes the set of parameter keys shared by all selected entities."""
        param_sets = []

        for ent in self.comparison_entities:
            subkeys: set[str] = set()

            for p in ent.parameters:
                idx = p.key.count(".") - 1
                param_id = p.key.split(".", idx)[idx]

                subkeys.add(param_id)

                if param_id not in self.param_name_lookup:
                    self.param_name_lookup[param_id] = p.display_name

            param_sets.append(subkeys)
        if not param_sets:
            return 
        self.common_parameters = set.intersection(*param_sets)

    def normalize_chart_data(self):
        """Normalises each chart column by its maximum value so series are comparable."""
        if not self.chart_data:
            return

        for cat_idx in range(len(self.categories)):
            max_cat_value = float("-inf")
            for series in self.chart_data:
                if max_cat_value < series.raw_values[cat_idx]:
                    max_cat_value = series.raw_values[cat_idx]
            for series in self.chart_data:
                if max_cat_value > 0:
                    series.values[cat_idx] = series.raw_values[cat_idx] / max_cat_value

    def on_balance_file_changed(self, balance_file: BalanceFile):
        self.current_balance_file = balance_file
        self.reload_chart_data()

    def reload_chart_data(self):
        """Rebuilds chart series from the current balance file and selected entities."""
        categories = []
        series = []

        self.set_common_parameters()

        if self.current_balance_file:
            for ent in self.comparison_entities:
                data = ChartData(ent.display_name, [], [])
                for param in sorted(self.common_parameters, key=lambda pid: self.param_name_lookup.get(pid, pid).lower()):
                    value = self.current_balance_file.values.get(ent.key + "." + param, None)
                    data.values.append(0)
                    data.raw_values.append(value)
                    param_name = self.param_name_lookup.get(param, param)
                    if param_name not in categories:
                        categories.append(param_name)
                series.append(data)

        self.categories = categories
        self.chart_data = series
        self.normalize_chart_data()

        self.comparison_entity_selection_changed.emit()
