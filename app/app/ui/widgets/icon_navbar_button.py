#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: icon_navbar_button.py
Author: Jonas Bordewick
Date: 12.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

from app.ui.widgets.hover_tooltip import HoverTooltip


class NavbarIconButtonGroup:
    """Manages a set of NavbarIconButtons so only one is active at a time."""

    def __init__(self):
        self.buttons = []

    def add(self, button: 'NavbarIconButton'):
        self.buttons.append(button)
        button.clicked.connect(lambda: self.setActive(button))

    def setActive(self, button: 'NavbarIconButton'):
        for btn in self.buttons:
            btn.setActive(btn is button)

class NavbarIconButton(QPushButton):
    """Icon button for the navigation bar with a delayed custom HoverTooltip."""
    def __init__(self, icon_path: str, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
                 tooltip: HoverTooltip = None):
        super().__init__()
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(16, 16))

        self._alignment = alignment
        if alignment == Qt.AlignmentFlag.AlignLeft:
            self._offset = QPoint(9, 0)
        else:
            self._offset = QPoint(6, 0)

        self.setFixedSize(26, 26)
        self.setProperty("class", "icon-button")

        self.setProperty("active", False)

        self._tooltip = tooltip

        self._show_timer = QTimer(self)
        self._show_timer.setSingleShot(True)
        self._show_timer.timeout.connect(self._show_tooltip)


    def enterEvent(self, event):
        super().enterEvent(event)
        self._show_timer.start(100)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._show_timer.stop()
        if self._tooltip:
            self._tooltip.hide()

    def _show_tooltip(self):
        if not self._tooltip:
            return
        self._tooltip.showNear(self, alignment=self._alignment, offset=self._offset)

    def setActive(self, active: bool):
        if self.property("active") == active:
            return
        self.setProperty("active", active)

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()