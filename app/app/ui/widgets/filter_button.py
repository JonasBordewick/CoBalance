#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: filter_button.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class FilterButton(QWidget):

    triggered = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setProperty("class", "filter-button")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        self.setFixedSize(100, 40)

        self.icon = QLabel("❌")
        self.icon.setObjectName("leadingIcon")
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Filter")
        self.label.setObjectName("filterLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon)
        layout.addWidget(self.label, stretch=1)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.triggered.emit()
        super().mousePressEvent(event)