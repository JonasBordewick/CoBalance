#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: comparison_view.py
Author: Jonas Bordewick
Date: 21.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QModelIndex, QItemSelectionModel
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QBoxLayout, QFrame, QTableView, QPushButton, \
    QHeaderView, QRadioButton, QStackedWidget

from app.models.entity_table_model import EntityTableModel, EntityTableProxyModel
from app.models.selected_entity_table_model import SelectedEntityTableModel
from app.ui.widgets import ControlPanel, BarChartWidget, RadarChartWidget
from app.viewmodels import AppViewModel, BalanceViewModel


class EntityComparisonView(QWidget):
    def __init__(self, app_vm: AppViewModel, balance_vm: BalanceViewModel):
        super().__init__()

        self.setProperty("class", "comparison-view")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._app_vm = app_vm
        self._balance_vm = balance_vm

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(3)

        self._left_panel, self._left_layout = self._build_panel()
        self._right_panel, self._right_layout = self._build_panel()

        self._layout.addWidget(self._left_panel)
        self._layout.addWidget(self._right_panel, stretch=1)

        self._build_entity_table(self._left_panel)
        self._build_selected_entity_table(self._right_panel)
        control_panel = ControlPanel()
        control_panel.search_bar.text_changed.connect(lambda text: self.entity_table_proxy.setFilterRegularExpression(text))
        self._left_layout.addWidget(control_panel)
        self._left_layout.addWidget(self.entity_table)

        self._balance_vm.file_loaded.connect(self.load_balance)


        self._right_layout.addWidget(self._build_chart_control_bar())
        self._right_layout.addWidget(self._build_chart_stack(), stretch=1)
        self._right_layout.addWidget(self.selected_entity_table, stretch=1)

    def _build_panel(self) -> (QWidget, QBoxLayout):
        panel = QWidget(self)
        panel.setProperty("class", "comparison-panel")
        panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QVBoxLayout(panel)
        return panel, layout

    def _build_entity_table(self, parent: QWidget):
        table = QTableView(parent=parent)
        table.setProperty("class", "comparison-table")
        table.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableView.SelectionMode.MultiSelection)

        self.entity_table = table  # Store reference to the table for later use

        self.entity_table_model = EntityTableModel(self._balance_vm, [])
        self.entity_table_proxy = EntityTableProxyModel()
        self.entity_table_proxy.setSourceModel(self.entity_table_model)
        self.entity_table.setModel(self.entity_table_proxy)

        selection_model = table.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _build_selected_entity_table(self, parent: QWidget):
        table = QTableView(parent=parent)
        table.setProperty("class", "comparison-table")
        table.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(False)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QTableView.SelectionMode.NoSelection)
        table.horizontalHeader().setStretchLastSection(True)

        self.selected_entity_table = table  # Store reference to the selected entity table for later use

        self.selected_entity_model = SelectedEntityTableModel(balance_vm=self._balance_vm, app_vm=self._app_vm)
        self.selected_entity_table.setModel(self.selected_entity_model)

        header = table.horizontalHeader()
        for i in range(header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def load_balance(self):
        if not self._balance_vm.file:
            return
        file = self._balance_vm.file
        if file is None:
            return
        rows = file.build_entity_rows()
        self.entity_table_model.set_rows(rows)
        self.selected_entity_model.set_balance()

    def _build_chart_stack(self) -> QWidget:
        chart = BarChartWidget(app_vm=self._app_vm, balance_vm=self._balance_vm, parent=self._right_panel)
        radar = RadarChartWidget(app_vm=self._app_vm, balance_vm=self._balance_vm, parent=self._right_panel)

        stack = QStackedWidget()

        stack.addWidget(chart)
        stack.addWidget(radar)

        self._app_vm.comparison_chart_type_changed.connect(lambda ct: stack.setCurrentIndex(int(ct)))
        stack.setCurrentIndex(int(self._app_vm.chart_type))

        return stack

    def _build_chart_control_bar(self):
        control_bar = QWidget()
        control_bar.setProperty("class", "chart-control-bar")
        control_bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QHBoxLayout(control_bar)
        layout.setContentsMargins(6, 5, 6, 5)
        layout.setSpacing(10)

        layout.addStretch()

        bar_chart_radio = QRadioButton("Bar Chart")
        radar_chart_radio = QRadioButton("Radar Chart")
        if self._app_vm.chart_type == self._app_vm.chart_type.BAR:
            bar_chart_radio.setChecked(True)
        else:
            radar_chart_radio.setChecked(True)

        bar_chart_radio.toggled.connect(
            lambda checked:
            self._app_vm.set_comparison_chart_type(self._app_vm.chart_type.BAR) if checked else None
        )
        radar_chart_radio.toggled.connect(
            lambda checked:
            self._app_vm.set_comparison_chart_type(self._app_vm.chart_type.RADAR) if checked else None
        )

        layout.addWidget(bar_chart_radio)
        layout.addWidget(radar_chart_radio)
        self.selected_entities_label = QLabel("")
        layout.addWidget(self.selected_entities_label)

        return control_bar

    def on_selection_changed(self):
        selection_model = self.entity_table.selectionModel()
        indexes = selection_model.selectedRows()

        selected_entities = []

        for index in indexes:
            source_index = self.entity_table_proxy.mapToSource(index)
            row_obj = self.entity_table_model.row_at(source_index.row())
            if not row_obj:
                return
            selected_entities.append(row_obj.entity_id)

        self._app_vm.set_selected_comparison_entities(selected_entities)
        self.selected_entity_model.update_table_model()
        header = self.selected_entity_table.horizontalHeader()
        for i in range(header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)