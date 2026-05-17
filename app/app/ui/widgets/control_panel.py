#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: control_panel.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from app.ui.widgets import SearchBar, FilterButton
from app.viewmodels import AppViewModel, BalanceViewModel


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setProperty("class", "control-bar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 5, 6, 5)
        layout.setSpacing(10)

        layout.addStretch()
        layout.addWidget(QLabel("Search:"))
        self.search_bar = SearchBar(self)
        layout.addWidget(self.search_bar)
