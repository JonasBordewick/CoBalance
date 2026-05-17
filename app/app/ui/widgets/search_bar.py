#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: search_bar.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton


class SearchBar(QWidget):

    text_changed = pyqtSignal(str)
    cleared = pyqtSignal()

    def __init__(self, parent=None, placeholder: str = "Search..."):
        super().__init__(parent)

        self.setProperty("class", "search-bar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setFixedSize(280, 40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        self.icon = QLabel("🔎")
        self.icon.setObjectName("leadingIcon")
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input = QLineEdit()
        self.input.setObjectName("searchInput")
        self.input.setPlaceholderText(placeholder)
        self.input.textChanged.connect(self._on_text_changed)

        self.clear_btn = QPushButton("❌")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setFixedSize(24, 24)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear)
        self.clear_btn.setVisible(False)

        layout.addWidget(self.icon)
        layout.addWidget(self.input, stretch=1)
        layout.addWidget(self.clear_btn)


    def _on_text_changed(self, text):
        self.clear_btn.setVisible(len(text) > 0)
        self.text_changed.emit(text)

    def clear(self):
        if self.input.text():
            self.input.clear()
        self.cleared.emit()

    def text(self) -> str:
        return self.input.text()

    def set_text(self, text: str):
        self.input.setText(text)

    def set_placeholder(self, text: str):
        self.input.setPlaceholderText(text)

    def set_focus(self):
        self.input.setFocus()

