#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: radar_chart_widget.py
Author: Jonas Bordewick
Date: 22.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from app.viewmodels import BalanceViewModel, AppViewModel

from .helper import radar_factory


class RadarChartWidget(QWidget):
    def __init__(self, app_vm: AppViewModel, balance_vm: BalanceViewModel, parent=None):
        super().__init__(parent)

        self._app_vm = app_vm
        self._balance_vm = balance_vm

        self.figure = Figure(dpi=100, constrained_layout=False)
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self._balance_vm.file_loaded.connect(self._render)
        self._app_vm.comparison_entity_selection_changed.connect(self._render)
        self._balance_vm.balance_file_changed.connect(self._render)

    def _render(self):
        self.figure.clear()

        if not self._app_vm.categories or not self._app_vm.chart_data or len(self._app_vm.categories) <= 2:
            ax = self.figure.add_subplot(111)
            ax.set_axis_off()
            self.canvas.draw_idle()
            return

        categories: list[str] = self._app_vm.categories
        series = self._app_vm.chart_data

        n_cat = len(categories)
        n_series = len(series)

        for s in series:
            if len(s.values) != n_cat:
                raise ValueError(f"Series '{s.name}' has {len(s.values)} values, but expected {n_cat} (number of categories).")

        theta = radar_factory(n_cat, frame='polygon')
        ax = self.figure.add_subplot(111, projection='radar')

        ax.set_ylim(0.0, 1.1)
        ax.grid(True, linewidth=0.8, alpha=0.75)

        ax.set_yticklabels([])
        ax.set_varlabels(categories)

        ax.tick_params(axis="x", pad=12.5)

        ax.spines["polar"].set_alpha(0.25)

        for s in series:
            ax.plot(theta, s.values, linewidth=2.0, label=s.name)
            ax.fill(theta, s.values, alpha=0.25)

        ax.set_xticklabels(categories, fontsize=9, wrap=True)
        handles, labels = ax.get_legend_handles_labels()

        self.figure.legend(
            handles,
            labels,
            loc="upper left",
            bbox_to_anchor=(0.02, 0.5),
            frameon=False,
            fontsize=9,
            handlelength=1.6,
            handletextpad=0.6
        )

        self.canvas.draw_idle()