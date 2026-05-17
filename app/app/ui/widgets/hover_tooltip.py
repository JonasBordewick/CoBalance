#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: hover_tooltip.py
Author: Jonas Bordewick
Date: 12.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPoint


class HoverTooltip(QFrame):
    """Custom styled tooltip window shown near a trigger widget on hover.

    Uses Qt.WindowType.ToolTip so the OS treats it as a popup. On Wayland a
    transient parent must be set before show() — see showNear().
    """
    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent, Qt.WindowType.ToolTip)

        self.setProperty("class", "hover-tooltip")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._text = QLabel(text)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self._text)

        self._pointer_size = 8

        self.hide()

    def showNear(self, anchor_widget: QWidget, offset: QPoint = QPoint(10, 10), alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        self.adjustSize()

        if alignment == Qt.AlignmentFlag.AlignLeft:
            anchor_pos = anchor_widget.mapToGlobal(anchor_widget.rect().topRight())
        else:
            anchor_pos = anchor_widget.mapToGlobal(anchor_widget.rect().topLeft())

        y = anchor_widget.mapToGlobal(anchor_widget.rect().center()).y() - self.height() // 2

        if alignment == Qt.AlignmentFlag.AlignLeft:
            x = anchor_pos.x() + offset.x()
        else:
            x = anchor_pos.x() - self.width() - offset.x()

        y = y + offset.y()

        self.move(x, y)

        # Wayland requires a transientParent on popup windows.
        # winId() forces creation of the native handle before show().
        self.winId()
        own_handle = self.windowHandle()
        parent_handle = anchor_widget.window().windowHandle()
        if own_handle and parent_handle:
            own_handle.setTransientParent(parent_handle)

        self.show()
