#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: content_area.py
Author: Jonas Bordewick
Date: 12.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget

from app.ui.views.parameter_view import ParameterView
from app.ui.views.comparison_view import EntityComparisonView
from app.ui.views.logs_view import LogsView
from app.viewmodels import AppViewModel, BalanceViewModel, LogsExplorerViewModel, ProjectContextViewModel
from app.viewmodels.job_view_model import JobViewModel


class ContentArea(QWidget):
    def __init__(
            self,
            project_context_view_model: ProjectContextViewModel,
            app_view_model: AppViewModel,
            balance_view_model: BalanceViewModel,
            logs_explorer_view_model: LogsExplorerViewModel,
            job_view_model: JobViewModel,
    ):
        super().__init__()
        self.project_context_view_model = project_context_view_model
        self.app_view_model = app_view_model
        self.balance_view_model = balance_view_model
        self.logs_explorer_view_model = LogsExplorerViewModel
        self.logs_group_view_model = logs_explorer_view_model.logs_group_view_model
        self.job_view_model = job_view_model

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Placeholder pages
        self.stack.addWidget(ParameterView(app_view_model, balance_view_model, job_view_model))
        self.stack.addWidget(EntityComparisonView(app_view_model, balance_view_model))
        self.stack.addWidget(LogsView(app_view_model, logs_explorer_view_model))

        # VM -> UI
        self.project_context_view_model.screen_changed.connect(self.stack.setCurrentIndex)

        # Initial sync
        self.stack.setCurrentIndex(int(self.project_context_view_model.current_screen))

    def _page(self, title: str) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(label)

        return w