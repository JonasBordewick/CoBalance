#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: bar_chart_widget.py
Author: Jonas Bordewick
Date: 22.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from app.viewmodels import BalanceViewModel, AppViewModel


class BarChartWidget(QWidget):
    def __init__(self, app_vm: AppViewModel, balance_vm: BalanceViewModel, parent=None):
        super().__init__(parent)

        self._app_vm = app_vm
        self._balance_vm = balance_vm

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.figure.tight_layout(pad=1.2)

        self._balance_vm.file_loaded.connect(self._render)
        self._app_vm.comparison_entity_selection_changed.connect(self._render)
        self._balance_vm.balance_file_changed.connect(self._render)

        self._render()

    def _render(self):
        self.ax.clear()

        if not self._app_vm.categories or not self._app_vm.chart_data:
            self.ax.set_axis_off()
            self.canvas.draw_idle()
            return

        categories: list[str] = self._app_vm.categories
        series = self._app_vm.chart_data

        n_cat = len(categories)
        n_series = len(series)

        for s in series:
            if len(s.values) != n_cat:
                raise ValueError(f"Series '{s.name}' has {len(s.values)} values, but expected {n_cat} (number of categories).")

        base_y = list(range(n_cat))

        group_height = 0.8
        bar_height = group_height / max(n_series, 1)

        offsets = []
        start = -group_height / 2 + bar_height / 2
        for i in range(n_series):
            offsets.append(start + i * bar_height)

        bars_by_series = []
        for si, s in enumerate(series):
            ys = [y + offsets[si] for y in base_y]
            b = self.ax.barh(
                ys,
                s.values,
                height=bar_height * 0.92,
                label=s.name,
            )
            bars_by_series.append(b)


        self.ax.set_yticks(base_y)
        self.ax.set_yticklabels(categories, fontsize=12, fontweight="bold")
        self.ax.invert_yaxis()  # top-to-bottom like in your mock

        for spine in ["top", "right", "left", "bottom"]:
            self.ax.spines[spine].set_visible(False)

        self.ax.xaxis.grid(True, linestyle="-", linewidth=0.6, alpha=0.25)
        self.ax.set_axisbelow(True)

        self.ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
        self.ax.tick_params(axis="y", length=0)

        # Legend bottom center (like mock)
        self.ax.legend(
            loc="lower center",
            bbox_to_anchor=(0.5, -0.10),
            ncol=min(n_series, 7),
            frameon=False,
            fontsize=9,
            handlelength=1.0,
            handletextpad=0.4,
            columnspacing=1.0,
        )

        self.figure.tight_layout(pad=1.2)
        self.canvas.draw_idle()

