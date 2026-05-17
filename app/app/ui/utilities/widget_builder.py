#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: widget_builder.py
Author: Jonas Bordewick
Date: 15.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QHBoxLayout, QBoxLayout


def build_widget_and_layout(parent: QWidget = None, orientation: Qt.Orientation = Qt.Orientation.Vertical) -> tuple[QWidget, QBoxLayout]:
    widget = QWidget(parent)
    if orientation == Qt.Orientation.Vertical:
        layout = QVBoxLayout(widget)
    else:
        layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(1)
    return widget, layout
