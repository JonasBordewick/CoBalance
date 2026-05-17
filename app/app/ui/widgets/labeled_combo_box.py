#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: #labeled_combo_box.py
Author: Jonas Bordewick
Date: 15.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel


class LabeledComboBox(QWidget):
    def __init__(self, label: str, parent=None, items: list[tuple[str, str]] = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.label = QLabel(label, self)
        self.combo = QComboBox(self)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)

        if items is not None:
            for item in items:
                self.combo.addItem(item[0], item[1])