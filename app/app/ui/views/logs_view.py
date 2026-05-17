#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_view.py
Author: Jonas Bordewick
Date: 08.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTableView, QHeaderView, QBoxLayout, \
    QInputDialog, QMessageBox, QMenu, QListWidget, QAbstractItemView, QComboBox

from app.models.logs_table_model import LogsTableModel, LogsTableProxyModel
from app.models.logs_table_row import LogsTableRow
from app.ui.delegates import GroupDelegate
from app.ui.utilities import create_group_from_selection_via_dialog, rename_group_via_dialog, build_widget_and_layout
from app.ui.widgets import LogChartWidget, LabeledComboBox
from app.viewmodels import AppViewModel, LogsExplorerViewModel


class LogsView(QWidget):
    def __init__(self, app_view_model: AppViewModel, logs_explorer_view_model: LogsExplorerViewModel):
        super().__init__()

        self._app_view_model = app_view_model
        self._logs_explorer_view_model = logs_explorer_view_model
        self._logs_group_view_model = logs_explorer_view_model.logs_group_view_model

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(3)

        self.top_panel, self._top_layout = self._build_panel(orientation=Qt.Orientation.Horizontal)
        self._bottom_panel, self._bottom_layout = self._build_panel()

        self.top_left_panel, self._top_left_layout = self._build_panel()
        self.top_right_panel = self._build_parameter_panel()

        self._top_layout.addWidget(self.top_left_panel, stretch=1)
        self._top_layout.addWidget(self.top_right_panel, stretch=1)

        self._layout.addWidget(self.top_panel, stretch=1)
        self._layout.addWidget(self._bottom_panel, stretch=1)

        self._build_logs_table()
        self._top_left_layout.addWidget(self.logs_table)

        self._bottom_label = QLabel(self)
        self._bottom_layout.addWidget(self._bottom_label)

        self.log_chart_widget = LogChartWidget(self)
        self._bottom_layout.addWidget(self.log_chart_widget)

        self._logs_explorer_view_model.logs_changed.connect(self.load_logs)
        self._logs_group_view_model.groups_changed.connect(self.load_logs)

        self._logs_explorer_view_model.log_selection_changed.connect(self.update_bottom_status)
        self._logs_explorer_view_model.plot_settings_changed.connect(self.update_bottom_status)
        self._logs_explorer_view_model.selected_parameters_changed.connect(self.update_bottom_status)
        self._logs_explorer_view_model.log_selection_changed.connect(self.update_bottom_plot)
        self._logs_explorer_view_model.selected_parameters_changed.connect(self.update_bottom_plot)
        self._logs_explorer_view_model.plot_settings_changed.connect(self.update_bottom_plot)

    def _build_panel(self, orientation: Qt.Orientation = Qt.Orientation.Vertical) -> (QWidget, QBoxLayout):
        panel = QWidget(self)
        panel.setProperty("class", "log-panel")
        panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        if orientation == Qt.Orientation.Vertical:
            layout = QVBoxLayout(panel)
        else:
            layout = QHBoxLayout(panel)
        return panel, layout

    def _build_logs_table(self):
        table = QTableView(self)
        table.setProperty("class", "logs-table")
        table.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)

        self.logs_table = table  # Store reference to the table for later use

        self.logs_table_model = LogsTableModel(self._logs_explorer_view_model, [])
        self.logs_table_proxy = LogsTableProxyModel()
        self.logs_table_proxy.setSourceModel(self.logs_table_model)
        self.logs_table.setModel(self.logs_table_proxy)
        self.logs_table.setItemDelegateForColumn(
            LogsTableModel.COL_GROUP,
            GroupDelegate(
                self._logs_group_view_model,
                parent=self.logs_table
            )
        )
        self.logs_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.logs_table.customContextMenuRequested.connect(self._on_logs_table_context_menu)

        selection_model = table.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        table.sortByColumn(LogsTableModel.COL_TIMESTAMP, Qt.SortOrder.DescendingOrder)

    def _build_parameter_panel(self) -> QWidget:
        panel, layout = self._build_panel()

        top_row, top_row_layout = build_widget_and_layout(panel)

        self._parameter_panel_title = QLabel("Parameters")
        top_row_layout.addWidget(self._parameter_panel_title)

        self._parameter_panel_list = QListWidget(panel)
        self._parameter_panel_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        top_row_layout.addWidget(self._parameter_panel_list)

        self._logs_explorer_view_model.log_selection_changed.connect(self.on_log_selection_changed)
        self._logs_explorer_view_model.selected_parameters_changed.connect(self.on_selected_parameters_changed)
        self._parameter_panel_list.itemSelectionChanged.connect(self.on_parameter_selection_changed)

        layout.addWidget(top_row, 2)

        self.value_mode = LabeledComboBox(
            "Value Mode",
            panel,
            items=[
              ("Raw Values", "raw"),
              ("Value per Second", "per_second")
            ]
        )
        self.value_mode.combo.setToolTip("Raw Values: plot the absolute logged values.\nValue per Second: normalize each value by the time elapsed, useful for comparing runs of different durations.")

        self.chart_type = LabeledComboBox(
            "Chart Type",
            panel,
            items=[
              ("Line Chart", "line"),
              ("Boxplot", "box")
            ]
        )
        self.chart_type.combo.setToolTip("Line Chart: shows value progression over time.\nBoxplot: shows the distribution across all selected runs.")

        self.compare_mode = LabeledComboBox(
            "Compare Mode",
            panel,
            items=[
                ("Individual", "individual"),
                ("Grouped", "grouped")
            ]
        )
        self.compare_mode.combo.setToolTip("Individual: plot each selected log file as a separate series.\nGrouped: aggregate logs by their group and plot one series per group.")

        self.group_aggregation_mode = LabeledComboBox(
            "Group Aggregation Mode",
            panel,
            items=[
                ("Mean", "mean"),
                ("Median", "median"),
                ("Min", "min"),
                ("Max", "max"),
                ("Sum", "sum")
            ]
        )
        self.group_aggregation_mode.combo.setToolTip("How individual log values are combined within a group before plotting. Only active in Grouped compare mode.")

        layout.addWidget(self.value_mode)
        layout.addWidget(self.chart_type)
        layout.addWidget(self.compare_mode)
        layout.addWidget(self.group_aggregation_mode)

        self.value_mode.combo.currentIndexChanged.connect(self._on_value_mode_changed)
        self.value_mode.combo.setCurrentIndex(self.value_mode.combo.findData(self._logs_explorer_view_model.selected_value_mode))

        self.chart_type.combo.currentIndexChanged.connect(self._on_chart_type_changed)
        self.chart_type.combo.setCurrentIndex(self.chart_type.combo.findData(self._logs_explorer_view_model.selected_chart_type))

        self.compare_mode.combo.currentIndexChanged.connect(self.on_compare_mode_changed)
        self.compare_mode.combo.setCurrentIndex(
            self.compare_mode.combo.findData(self._logs_explorer_view_model.selected_compare_mode))

        self.group_aggregation_mode.combo.currentIndexChanged.connect(self.on_group_aggregation_changed)
        self.group_aggregation_mode.combo.setCurrentIndex(
            self.group_aggregation_mode.combo.findData(self._logs_explorer_view_model.selected_group_aggregation))

        self.update_plot_settings_ui()

        return panel

    def load_logs(self):
        self.logs_table_model.set_rows(self._logs_explorer_view_model.build_logs_rows())

    def on_selection_changed(self):
        selection_model = self.logs_table.selectionModel()
        indexes = selection_model.selectedRows()

        selected_rows: list[str] = []

        for index in indexes:
            source_index = self.logs_table_proxy.mapToSource(index)
            row = self.logs_table_model.row_at(source_index.row())
            if not row:
                return
            selected_rows.append(row.file_name)

        self._logs_explorer_view_model.set_selected_log_files(selected_rows)

    def on_parameter_selection_changed(self):
        keys = [item.text() for item in self._parameter_panel_list.selectedItems()]
        self._logs_explorer_view_model.set_selected_parameter_keys(keys)

    def on_log_selection_changed(self):
        self._parameter_panel_list.clear()
        all_keys = self._logs_explorer_view_model.selected_keys_intersection
        selected_keys = self._logs_explorer_view_model.selected_parameter_keys

        if not all_keys:
            self._parameter_panel_title.setText("Parameters")
            self._logs_explorer_view_model.set_selected_parameter_keys([])
            return

        self._parameter_panel_title.setText(f"Parameters ({len(selected_keys)} selected)")
        self._parameter_panel_list.addItems(all_keys)
        self._logs_explorer_view_model.set_selected_parameter_keys([])

    def on_selected_parameters_changed(self):
        selected_keys = self._logs_explorer_view_model.selected_parameter_keys
        self._parameter_panel_title.setText(f"Parameters ({len(selected_keys)} selected)")

    def _on_value_mode_changed(self):
        value = self.value_mode.combo.currentData()
        self._logs_explorer_view_model.set_selected_value_mode(value)

    def _on_chart_type_changed(self):
        value = self.chart_type.combo.currentData()
        self._logs_explorer_view_model.set_selected_chart_type(value)

    def on_compare_mode_changed(self):
        value = self.compare_mode.combo.currentData()
        self._logs_explorer_view_model.set_selected_compare_mode(value)
        self.update_plot_settings_ui()

    def on_group_aggregation_changed(self):
        value = self.group_aggregation_mode.combo.currentData()
        self._logs_explorer_view_model.set_selected_group_aggregation(value)

    def update_plot_settings_ui(self):
        is_grouped = self._logs_explorer_view_model.selected_compare_mode == "grouped"
        self.group_aggregation_mode.setEnabled(is_grouped)

    def update_bottom_status(self):
        vm = self._logs_explorer_view_model

        error = vm.get_plot_validation_error()

        lines = []

        if error:
            lines.append("Plot not possible:")
            lines.append(error)
        self._bottom_label.setText("\n".join(lines))

    def update_bottom_plot(self):
        vm = self._logs_explorer_view_model

        error = vm.get_plot_validation_error()
        if error:
            self.log_chart_widget.clear()
            return

        plot_data = vm.build_chart_data()

        if vm.selected_chart_type == "line":
            self.log_chart_widget.set_line_chart_data(plot_data)
            return
        elif vm.selected_chart_type == "box":
            self.log_chart_widget.set_boxplot_data(plot_data)
            return
        else:
            self.log_chart_widget.clear()

    def _on_logs_table_context_menu(self, pos):
        index = self.logs_table.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self)

        selected_count = self._logs_explorer_view_model.count_of_selected_logs
        selected_log_names = list(self._logs_explorer_view_model.selected_log_names)

        action_create_group = menu.addAction("Create Group From Selection")
        action_remove_from_group = menu.addAction("Remove From Group")
        action_rename_group = menu.addAction("Rename Group")
        action_delete_group = menu.addAction("Delete Group")

        action_create_group.setEnabled(selected_count > 0)

        any_grouped = any(
            self._logs_group_view_model.get_group_for_log(log_name) is not None
            for log_name in selected_log_names
        )
        action_remove_from_group.setEnabled(any_grouped)

        current_group = None
        if selected_count == 1:
            log_name = selected_log_names[0]
            current_group = self._logs_group_view_model.get_group_for_log(log_name)

        action_rename_group.setEnabled(current_group is not None)
        action_delete_group.setEnabled(current_group is not None)

        chosen_action = menu.exec(self.logs_table.viewport().mapToGlobal(pos))
        if chosen_action is None:
            return

        if chosen_action == action_create_group:
            create_group_from_selection_via_dialog(parent=self, logs_explorer_view_model=self._logs_explorer_view_model)

        elif chosen_action == action_remove_from_group:
            self._logs_explorer_view_model.remove_selected_logs_from_groups()

        elif chosen_action == action_rename_group and current_group is not None:
            rename_group_via_dialog(parent=self, logs_group_view_model=self._logs_group_view_model, group=current_group)

        elif chosen_action == action_delete_group and current_group is not None:
            self._logs_group_view_model.delete_group(current_group.id)
