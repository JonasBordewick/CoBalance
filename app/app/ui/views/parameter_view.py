#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: parameter_view.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView, QFrame, QHBoxLayout, QLabel, QStyledItemDelegate

from app.models import ParameterTableModel, ParameterTableFilterProxy, ParameterTableRow
from app.ui.widgets import ControlPanel, SearchBar
from app.viewmodels import AppViewModel, BalanceViewModel
from app.viewmodels.job_view_model import JobViewModel


class ParameterView(QWidget):
    def __init__(self, app_vm: AppViewModel, balance_vm: BalanceViewModel, job_vm: JobViewModel):
        super().__init__()

        self.setProperty("class", "parameter-view")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(3)

        self._app_vm = app_vm
        self._balance_vm = balance_vm
        self._job_vm = job_vm

        self._control_panel = ControlPanel()
        self._control_panel.search_bar.text_changed.connect(self._on_search)
        self._layout.addWidget(self._control_panel, alignment=Qt.AlignmentFlag.AlignTop)

        table = self._build_parameter_table()

        self._layout.addWidget(table)

        self._balance_vm.file_loaded.connect(self.load_balance)
        self._balance_vm.balance_file_changed.connect(self.load_balance)

    def _on_search(self, text: str):
        # simple contains-search
        self.proxy.setFilterRegularExpression(text)

    def _build_control_bar(self) -> QWidget:
        widget = QWidget(self)
        widget.setProperty("class", "control-bar")
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        widget.setFixedHeight(50)

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 5, 6, 5)
        layout.setSpacing(10)
        widget.setLayout(layout)

        layout.addStretch()
        layout.addWidget(QLabel("Search:"))
        search_bar = SearchBar(self)
        search_bar.text_changed.connect(self._on_search)
        layout.addWidget(search_bar)

        return widget

    def _build_parameter_table(self) -> QWidget:
        widget = QFrame(self)
        widget.setProperty("class", "parameter-table")
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)
        widget.setLayout(layout)

        self.table = QTableView()
        self.table.setObjectName("parameterTable")
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.MultiSelection)

        # Model + Proxy
        self.model = ParameterTableModel(self._balance_vm, [])
        self.proxy = ParameterTableFilterProxy()
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)

        # nice defaults
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set Column Widths
        self.table.setColumnWidth(0, 260)  # Parameter
        self.table.setColumnWidth(1, 90)  # Value
        self.table.setColumnWidth(2, 220)  # Entity
        self.table.setColumnWidth(3, 180)  # Category

        selection_model = self.table.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table, stretch=1)
        layout.addStretch()
        return widget

    def load_balance(self):
        if not self._balance_vm.is_loaded:
            return
        file = self._balance_vm.file
        if file is None:
            return
        rows = file.build_parameter_rows()
        self.model.set_rows(rows)

    def on_selection_changed(self):

        selection_model = self.table.selectionModel()
        indexes = selection_model.selectedRows()

        selected_parameters: list[ParameterTableRow] = []

        for index in indexes:
            source_index = self.proxy.mapToSource(index)
            row_obj = self.model.row_at(source_index.row())
            if not row_obj:
                continue
            selected_parameters.append(row_obj)

        self._job_vm.select_parameters(selected_parameters)
