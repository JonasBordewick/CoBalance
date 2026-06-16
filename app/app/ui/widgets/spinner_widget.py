#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: spinner_widget.py
Author: Jonas Bordewick
Date: 16.06.2026
Contact: jonas.bordewick@uni-a.de
"""
import math

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget


class SpinnerWidget(QWidget):
    _DOT_COUNT = 8
    _INTERVAL_MS = 80

    def __init__(self, size: int = 16, parent=None):
        super().__init__(parent)
        self._size = size
        self._step = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self.setFixedSize(size, size)
        self.hide()

    def start(self):
        self._step = 0
        self.show()
        self._timer.start(self._INTERVAL_MS)

    def stop(self):
        self._timer.stop()
        self.hide()

    def _advance(self):
        self._step = (self._step + 1) % self._DOT_COUNT
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self._size / 2
        orbit = center * 0.62
        dot_r = center * 0.18

        for i in range(self._DOT_COUNT):
            age = (i - self._step) % self._DOT_COUNT
            alpha = int(255 * (1.0 - age / self._DOT_COUNT) ** 1.5)
            angle = (2 * math.pi / self._DOT_COUNT) * i
            x = center + orbit * math.cos(angle) - dot_r
            y = center + orbit * math.sin(angle) - dot_r

            painter.setBrush(QColor(80, 80, 80, alpha))
            painter.setPen(QColor(0, 0, 0, 0))
            painter.drawEllipse(int(x), int(y), int(dot_r * 2), int(dot_r * 2))
