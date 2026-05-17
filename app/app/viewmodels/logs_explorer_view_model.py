#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_explorer_view_model.py
Author: Jonas Bordewick
Date: 23.03.26
Contact: jonas.bordewick@uni-a.de
"""
import os

import pandas as pd
from PyQt6.QtCore import pyqtSignal, QObject

from app.domain.logs import LogsAnalysisService, AnalysisOptions
from app.enums import ValueMode, LogChartType, CompareMode, Aggregation
from app.io.watchers import DirectoryWatcherService
from app.models import LogsTableRow
from app.utilities import parse_log_file

from .logs_group_view_model import LogsGroupViewModel
from .project_context_view_model import ProjectContextViewModel


class LogsExplorerViewModel(QObject):
    """Manages the log explorer: discovery of log files, selection, and chart data assembly.

    Watches the logs directory for new files, parses selected logs into DataFrames,
    and delegates chart-data construction to LogsAnalysisService based on the
    current chart type, compare mode, and aggregation settings.
    """

    logs_changed = pyqtSignal()
    log_selection_changed = pyqtSignal()
    selected_parameters_changed = pyqtSignal()
    plot_settings_changed = pyqtSignal()

    file_watcher_key = "Logs"

    MAX_LINE_PARAMETERS = 4
    MAX_LINE_COMPARE_INDIVIDUAL = 5
    MAX_LINE_COMPARE_GROUPED = 5

    MAX_BOX_PARAMETERS = 1
    MAX_BOX_COMPARE_INDIVIDUAL = 10
    MAX_BOX_COMPARE_GROUPED = 10

    def __init__(
            self,
            file_watcher: DirectoryWatcherService,
            logs_group_view_model: LogsGroupViewModel,
            project_context_view_model: ProjectContextViewModel,
            parent = None
    ):
        super().__init__(parent)
        self._analysis_service = LogsAnalysisService()
        self._watcher = file_watcher
        self._logs_group_view_model = logs_group_view_model
        self._project_context_view_model = project_context_view_model

        self._logs_by_name: dict[str, str] = {}
        self._selected_log_names: set[str] = set()

        self._selected_logs_by_name_by_key: dict[str, dict[str, pd.DataFrame]] = {}

        self._selected_parameter_keys: list[str] = []

        self._selected_value_mode: str = "raw"
        self._selected_chart_type: str = "line"
        self._selected_compare_mode: str = "individual"
        self._selected_group_aggregation: str = "mean"

        self._watcher.watched_directory_changed.connect(self._on_watcher_directory_changed)
        self._project_context_view_model.project_changed.connect(
            self._on_open_project
        )

    # -----------------------------------------------------------------------------------------------
    # ------------------------------------------PROPERTIES-------------------------------------------
    # -----------------------------------------------------------------------------------------------

    @property
    def logs(self) -> dict[str, str]:
        return self._logs_by_name

    @property
    def count_of_selected_logs(self) -> int:
        return len(self._selected_log_names)

    @property
    def logs_group_view_model(self) -> LogsGroupViewModel:
        return self._logs_group_view_model

    @property
    def selected_keys_intersection(self) -> list[str]:
        if not self._selected_logs_by_name_by_key:
            return []
        key_sets = [set(logs_by_key.keys()) for logs_by_key in self._selected_logs_by_name_by_key.values()]
        intersection = set.intersection(*key_sets)
        return sorted(intersection)

    # Not needed for now, but could be useful in the future
    @property
    def selected_keys_union(self) -> list[str]:
        if not self._selected_logs_by_name_by_key:
            return []
        key_sets = [set(logs_by_key.keys()) for logs_by_key in self._selected_logs_by_name_by_key.values()]
        union = set.union(*key_sets)
        return sorted(union)

    @property
    def selected_value_mode(self) -> str:
        return self._selected_value_mode

    @property
    def selected_chart_type(self) -> str:
        return self._selected_chart_type

    @property
    def selected_compare_mode(self) -> str:
        return self._selected_compare_mode

    @property
    def selected_group_aggregation(self) -> str:
        return self._selected_group_aggregation

    @property
    def selected_log_names(self) -> set[str]:
        return self._selected_log_names

    @property
    def selected_parameter_keys(self) -> list[str]:
        return self._selected_parameter_keys


    # -----------------------------------------------------------------------------------------------
    # -------------------------------------------SETTERS---------------------------------------------
    # -----------------------------------------------------------------------------------------------

    def set_selected_log_files(self, files: list[str]):
        """Parses and caches the selected log files so chart data can be built without re-reading."""
        self._selected_log_names = set(files)
        self._selected_logs_by_name_by_key = {}

        for log_name in self._selected_log_names:
            file_path = self._logs_by_name.get(log_name, None)
            if file_path is None:
                continue
            logs_by_key = parse_log_file(file_path)
            self._selected_logs_by_name_by_key[log_name] = logs_by_key

        self.log_selection_changed.emit()

    def set_selected_parameter_keys(self, keys: list[str]):
        self._selected_parameter_keys = keys
        self.selected_parameters_changed.emit()

    def set_selected_value_mode(self, value_mode: str):
        if self._selected_value_mode == value_mode:
            return
        self._selected_value_mode = value_mode
        self.plot_settings_changed.emit()

    def set_selected_chart_type(self, chart_type: str):
        if self._selected_chart_type == chart_type:
            return
        self._selected_chart_type = chart_type
        self.plot_settings_changed.emit()

    def set_selected_compare_mode(self, compare_mode: str):
        if self._selected_compare_mode == compare_mode:
            return
        self._selected_compare_mode = compare_mode
        self.plot_settings_changed.emit()

    def set_selected_group_aggregation(self, aggregation: str):
        if self._selected_group_aggregation == aggregation:
            return
        self._selected_group_aggregation = aggregation
        self.plot_settings_changed.emit()

    # -----------------------------------------------------------------------------------------------
    # --------------------------------------------LOGS-----------------------------------------------
    # -----------------------------------------------------------------------------------------------

    def _on_open_project(self):
        self._logs_by_name.clear()
        logs_path = self._project_context_view_model.logs_directory
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        self._watcher.watch_directory(self.file_watcher_key, logs_path)
        self._logs_group_view_model.set_file_path(logs_path)
        self.load_logs(logs_path)

    def on_file_loaded(self, path: str):
        self._logs_by_name.clear()

        logs_path = os.path.join(os.path.dirname(path), "Logs")
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        self._watcher.watch_directory(self.file_watcher_key, logs_path)
        self._logs_group_view_model.set_file_path(logs_path)
        self.load_logs(logs_path)

    def load_logs(self, path):
        self._logs_by_name.clear()

        for file_name in os.listdir(path):
            if file_name.endswith(".jsonl"):
                file_path = os.path.join(path, file_name)
                self._logs_by_name[file_name] = file_path

        self.logs_changed.emit()

    def clear_logs(self):
        self._logs_by_name.clear()
        self.logs_changed.emit()

    def _on_watcher_directory_changed(self, key: str, path: str):
        if key == self.file_watcher_key:
            self.load_logs(path)

    def build_chart_data(self):
        """Delegates to the appropriate chart-data builder based on the selected chart type."""
        if self._selected_chart_type == "box":
            return self._build_box_plot_data()
        elif self._selected_chart_type == "line":
            return self._build_line_chart_data()
        self._project_context_view_model.on_error(f"Unknown chart type: {self._selected_chart_type}")
        raise ValueError(f"Unknown chart type: {self._selected_chart_type}")

    def _build_line_chart_data(self):
        options = self._create_analysis_options()

        if self._selected_compare_mode == "individual":
            return self._analysis_service.build_individual_line_chart_data(
                parameters=self._selected_parameter_keys,
                logs=self._selected_logs_by_name_by_key,
                options=options)
        elif self._selected_compare_mode == "grouped":
            return self._analysis_service.build_grouped_line_chart_data(
                parameters=self._selected_parameter_keys,
                logs=self._selected_logs_by_name_by_key,
                selected_groups=self._logs_group_view_model.get_selected_groups(self._selected_log_names),
                group_id_by_log_name=self._logs_group_view_model.group_id_by_log_name,
                options=options)
        self._project_context_view_model.on_error(f"Unknown compare mode: {self._selected_compare_mode}")
        raise ValueError(f"Unknown compare mode: {self._selected_compare_mode}")

    def _build_box_plot_data(self):
        options = self._create_analysis_options()

        if self._selected_compare_mode == "individual":
            return self._analysis_service.build_individual_boxplot_data(
                parameters=self._selected_parameter_keys,
                logs=self._selected_logs_by_name_by_key,
                options=options)
        elif self._selected_compare_mode == "grouped":
            return self._analysis_service.build_grouped_boxplot_data(
                parameters=self._selected_parameter_keys,
                logs=self._selected_logs_by_name_by_key,
                selected_groups=self._logs_group_view_model.get_selected_groups(self._selected_log_names),
                group_id_by_log_name=self._logs_group_view_model.group_id_by_log_name,
                options=options
            )
        self._project_context_view_model.on_error(f"Unknown compare mode: {self._selected_compare_mode}")
        raise ValueError(f"Unknown compare mode: {self._selected_compare_mode}")

    def _create_analysis_options(self) -> AnalysisOptions:
        return AnalysisOptions(
            value_mode=ValueMode(self._selected_value_mode),
            chart_type=LogChartType(self._selected_chart_type),
            compare_mode=CompareMode(self._selected_compare_mode),
            aggregation=Aggregation(self._selected_group_aggregation)
        )

    def build_logs_rows(self) -> list[LogsTableRow]:
        """Builds table rows for all known log files, using the file's mtime as the timestamp."""
        rows: list[LogsTableRow] = []

        for file_name, file_path in self.logs.items():
            rows.append(
                LogsTableRow(
                    file_name=file_name,
                    timestamp=os.path.getmtime(file_path),
                    file_path=file_path
                )
            )

        return rows

    def create_group_from_selection(self, name: str | None = None):
        self._logs_group_view_model.create_group_from_logs(list(self._selected_log_names), name)

    def remove_selected_logs_from_groups(self):
        self._logs_group_view_model.remove_logs_from_group(list(self._selected_log_names))

    # -----------------------------------------------------------------------------------------------
    # --------------------------------------INPUT VALIDATION-----------------------------------------
    # -----------------------------------------------------------------------------------------------

    def get_plot_validation_error(self) -> str | None:
        """Returns a human-readable error string if the current selection cannot be plotted, else None."""
        if self._selected_chart_type == "line":
            return self._get_line_chart_validation_error()
        if self._selected_chart_type == "box":
            return self._get_boxplot_validation_error()
        self._project_context_view_model.on_error(f"Unknown chart type: {self._selected_chart_type}")
        raise ValueError(f"Unknown chart type: {self._selected_chart_type}")

    def _get_line_chart_validation_error(self) -> str | None:
        return self._get_plot_validation_error(
            max_parameters=self.MAX_LINE_PARAMETERS,
            max_compare_individual=self.MAX_LINE_COMPARE_INDIVIDUAL,
            max_compare_grouped=self.MAX_LINE_COMPARE_GROUPED,
        )

    def _get_boxplot_validation_error(self) -> str | None:
        return self._get_plot_validation_error(
            max_parameters=self.MAX_BOX_PARAMETERS,
            max_compare_individual=self.MAX_BOX_COMPARE_INDIVIDUAL,
            max_compare_grouped=self.MAX_BOX_COMPARE_GROUPED,
        )

    def _get_plot_validation_error(self, max_parameters: int, max_compare_individual: int, max_compare_grouped: int) -> str | None:
        parameter_count = len(self._selected_parameter_keys)

        if parameter_count == 0:
            return "No parameters selected."

        if parameter_count > max_parameters:
            return (
                f"Too many parameters selected for plotting "
                f"({parameter_count}/{max_parameters})."
            )

        if self._selected_compare_mode == "individual":
            count = len(self._selected_log_names)

            if count == 0:
                return "No logs selected."

            if count > max_compare_individual:
                return (
                    f"Too many selected logs for individual mode "
                    f"({count}/{max_compare_individual})."
                )

            return None

        if self._selected_compare_mode == "grouped":
            if len(self._selected_log_names) == 0:
                return "No logs selected."

            if self._logs_group_view_model.has_ungrouped_selected_logs(self._selected_log_names):
                return "Grouped mode requires all selected logs to belong to a group."

            count = len(self._logs_group_view_model.get_selected_group_ids(self._selected_log_names))

            if count == 0:
                return "No groups available in current selection."

            if count > max_compare_grouped:
                return (
                    f"Too many groups for grouped mode "
                    f"({count}/{max_compare_grouped})."
                )

            return None

        self._project_context_view_model.on_error(f"Unknown compare mode: {self._selected_compare_mode}")
        raise ValueError(f"Unknown compare mode: {self._selected_compare_mode}")