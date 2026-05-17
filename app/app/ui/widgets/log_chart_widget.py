#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: log_chart_widget.py
Author: Jonas Bordewick
Date: 11.03.2026
Contact: jonas.bordewick@uni-a.de
"""

from __future__ import annotations

from itertools import cycle
from typing import Iterable, Any

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget, QApplication, QToolButton, QCheckBox
from matplotlib.ticker import MultipleLocator

from app.ui.utilities import build_widget_and_layout


class LogChartWidget(QWidget):
    LINE_STYLES: tuple[str, ...] = ("-", "--", "-.", ":")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._show_legend = False
        self._legends = []

        row, row_layout = build_widget_and_layout(self, orientation=Qt.Orientation.Horizontal)

        self._legend_toggle = QCheckBox(row)
        self._legend_toggle.setText("Show Legend")
        self._legend_toggle.setCheckable(True)
        self._legend_toggle.setChecked(False)
        self._legend_toggle.toggled.connect(self._on_legend_toggled)

        self._figure = Figure(constrained_layout=True)
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._toolbar = NavigationToolbar2QT(self._canvas, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        row_layout.addWidget(self._toolbar)
        row_layout.addWidget(self._legend_toggle)
        layout.addWidget(row)
        layout.addWidget(self._canvas)

        from matplotlib import colormaps
        self.cmap = colormaps["tab10"]

        self._axis = None
        self._max_t: float = 0.0
        self._min_x: float = 0.0
        self._min_width: float = 10.0
        self._fixed_ylim: tuple[float, float] | None = None
        self._is_clamping = False

        self._canvas.mpl_connect("scroll_event", self._on_scroll)

        self._hover_annotation = None
        self._boxplot_hover_items = []

        self._canvas.mpl_connect("motion_notify_event", self._on_hover)
        self._canvas.mpl_connect("figure_leave_event", self._on_figure_leave)

    def _on_legend_toggled(self, checked: bool):
        self._show_legend = checked

        for legend in self._legends:
            legend.set_visible(checked)

        self._canvas.draw_idle()

    def _on_hover(self, event):
        if self._hover_annotation is None:
            return

        visible = False

        for item in self._boxplot_hover_items:
            artist = item["artist"]
            contains, _ = artist.contains(event)
            if not contains:
                continue

            stats = item["stats"]
            text = (
                f"{item['label']}\n"
                f"MAX: {stats['max']:.2f}\n"
                f"MEDIAN: {stats['median']:.2f}\n"
                f"MIN: {stats['min']:.2f}"
            )

            ann = self._hover_annotation
            ann.xy = (event.xdata, event.ydata)
            ann.set_text(text)

            x_offset = 12
            y_offset = 12
            ha = "left"
            va = "bottom"

            canvas_width, canvas_height = self._canvas.get_width_height()

            lines = text.count("\n") + 1
            est_width = 160
            est_height = 18 * lines + 10

            mouse_x = event.x
            mouse_y = event.y

            if mouse_x + x_offset + est_width > canvas_width:
                x_offset = -12
                ha = "right"

            if mouse_y + y_offset + est_height > canvas_height:
                y_offset = -12
                va = "top"

            ann.set_ha(ha)
            ann.set_va(va)
            ann.set_position((x_offset, y_offset))
            ann.set_visible(True)

            visible = True
            break

        if not visible and self._hover_annotation.get_visible():
            self._hover_annotation.set_visible(False)

        self._canvas.draw_idle()

    def _on_figure_leave(self, event):
        if self._hover_annotation is not None and self._hover_annotation.get_visible():
            self._hover_annotation.set_visible(False)
            self._canvas.draw_idle()

    def clear(self):
        self._figure.clear()
        self._canvas.draw_idle()

    def set_line_chart_data(self, plot_data: dict[str, list[tuple[str, pd.DataFrame]]]):
        self._figure.clear()
        self._legends = []

        if not plot_data:
            self._canvas.draw_idle()
            return

        self._axis = self._figure.add_subplot(111)

        parameter_keys = list(plot_data.keys())

        parameter_style = {
            parameter_key: self.LINE_STYLES[i % len(self.LINE_STYLES)]
            for i, parameter_key in enumerate(parameter_keys)
        }

        all_labels: list[str] = []
        for series_list in plot_data.values():
            for label, _ in series_list:
                if label not in all_labels:
                    all_labels.append(label)

        label_to_color = {
            label: self.cmap(i % 10)
            for i, label in enumerate(all_labels)
        }

        max_t = 0.0
        for parameter_key in parameter_keys:
            series_list = plot_data[parameter_key]
            style = parameter_style[parameter_key]

            for label, df in series_list:
                if df is None or df.empty:
                    continue
                if "t" not in df.columns or "v" not in df.columns:
                    continue

                max_t = max(max_t, float(df["t"].max()))

                self._axis.plot(
                    df["t"],
                    df["v"],
                    color=label_to_color[label],
                    linestyle=style,
                    label=f"{parameter_key} | {label}",
                )

        self._max_t = max_t
        self._fixed_ylim = self._axis.get_ylim()

        self._axis.callbacks.connect("xlim_changed", self._on_xlim_changed)
        self._axis.callbacks.connect("ylim_changed", self._on_ylim_changed)

        initial_x_max = min(100, int(self._max_t)) if self._max_t > 0 else 100
        self._axis.set_xlim(0, initial_x_max)

        self._axis.xaxis.set_major_locator(MultipleLocator(10))
        self._axis.set_xlabel("time (s)")
        self._axis.set_ylabel("value")
        self._axis.grid(True, alpha=0.3)

        legend = self._axis.legend(loc="upper right", fontsize=8)
        if legend is not None:
            legend.set_visible(self._show_legend)
            self._legends.append(legend)

        self._canvas.draw_idle()

    def set_boxplot_data(self, plot_data: dict[str, list[tuple[str, list[float]]]]):
        self._figure.clear()
        self._legends = []
        self._boxplot_hover_items = []

        if not plot_data:
            self._canvas.draw_idle()
            return

        parameter_keys = list(plot_data.keys())
        parameter_count = len(parameter_keys)

        axes = self._figure.subplots(parameter_count, 1, squeeze=False)
        axes_flat = [row[0] for row in axes]

        cmap = self.cmap

        # gemeinsame Hover-Annotation
        first_axis = axes_flat[0]
        self._hover_annotation = first_axis.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="white", alpha=0.9),
            arrowprops=dict(arrowstyle="->", alpha=0.5),
        )
        self._hover_annotation.set_visible(False)

        for axis, parameter_key in zip(axes_flat, parameter_keys):
            samples = plot_data.get(parameter_key, [])

            labels: list[str] = []
            values: list[list[float]] = []

            for label, sample_values in samples:
                if not sample_values:
                    continue
                labels.append(label)
                values.append(sample_values)

            if values:
                label_to_color = {
                    label: cmap(i % 10)
                    for i, label in enumerate(labels)
                }

                bp = axis.boxplot(
                    values,
                    patch_artist=True,
                )

                # Boxen einfärben + Hover-Daten merken
                for i, (box, label, sample_values) in enumerate(zip(bp["boxes"], labels, values)):
                    color = label_to_color[label]
                    box.set_facecolor(color)
                    box.set_edgecolor(color)
                    box.set_alpha(0.5)

                    stats = {
                        "min": float(np.min(sample_values)),
                        "median": float(np.median(sample_values)),
                        "max": float(np.max(sample_values)),
                    }

                    self._boxplot_hover_items.append({
                        "artist": box,
                        "label": label,
                        "parameter": parameter_key,
                        "stats": stats,
                    })

                # Median-Linie
                for median in bp["medians"]:
                    median.set_color("black")
                    median.set_linewidth(1.5)

                # Whiskers und Caps
                for i, label in enumerate(labels):
                    color = label_to_color[label]

                    bp["whiskers"][2 * i].set_color(color)
                    bp["whiskers"][2 * i + 1].set_color(color)

                    bp["caps"][2 * i].set_color(color)
                    bp["caps"][2 * i + 1].set_color(color)

                # X-Achsen-Labels entfernen
                axis.set_xticks([])

                # Legend vorbereiten
                legend_handles = [
                    Patch(
                        facecolor=label_to_color[label],
                        edgecolor=label_to_color[label],
                        alpha=0.5,
                        label=label,
                    )
                    for label in labels
                ]

                legend = axis.legend(
                    handles=legend_handles,
                    loc="upper right",
                    frameon=True,
                    fontsize=8,
                )
                legend.set_visible(self._show_legend)
                self._legends.append(legend)

            axis.grid(True, alpha=0.3)

        self._canvas.draw_idle()


    def _on_scroll(self, event) -> Any:
        if self._axis is None or event.inaxes != self._axis:
            return

        axis = self._axis
        xmin, xmax = axis.get_xlim()
        width = xmax - xmin

        if width <= 0:
            return

        modifiers = QApplication.keyboardModifiers()
        is_ctrl = bool(modifiers & Qt.KeyboardModifier.ControlModifier)

        if is_ctrl:
            self._pan_x(event, axis, xmin, xmax, width)
        else:
            self._zoom_x(event, axis, xmin, xmax, width)

        self._update_x_locator(axis)
        self._canvas.draw_idle()

    def _pan_x(self, event, axis, xmin: float, xmax: float, width: float):
        step = width * 0.1

        if event.button == "up":
            new_xmin = xmin + step
            new_xmax = xmax + step
        elif event.button == "down":
            new_xmin = xmin - step
            new_xmax = xmax - step
        else:
            return

        new_xmin, new_xmax = self._clamp_x_limits(new_xmin, new_xmax, width)
        axis.set_xlim(new_xmin, new_xmax)

    def _zoom_x(self, event, axis, xmin: float, xmax: float, width: float):
        mouse_x = event.xdata
        if mouse_x is None:
            mouse_x = xmin + width / 2

        zoom_factor = 0.8 if event.button == "up" else 1.25

        new_width = width * zoom_factor
        max_width = max(self._max_t, self._min_width)
        new_width = max(self._min_width, min(new_width, max_width))

        relative_pos = (mouse_x - xmin) / width if width > 0 else 0.5

        new_xmin = mouse_x - relative_pos * new_width
        new_xmax = new_xmin + new_width

        new_xmin, new_xmax = self._clamp_x_limits(new_xmin, new_xmax, new_width)
        axis.set_xlim(new_xmin, new_xmax)

    def _clamp_x_limits(self, xmin: float, xmax: float, width: float) -> tuple[float, float]:
        if xmin < self._min_x:
            xmin = self._min_x
            xmax = xmin + width

        if self._max_t > 0 and xmax > self._max_t:
            xmax = self._max_t
            xmin = xmax - width

            if xmin < self._min_x:
                xmin = self._min_x
                xmax = xmin + width

        return xmin, xmax

    def _update_x_locator(self, axis):
        xmin, xmax = axis.get_xlim()
        width = xmax - xmin

        if width <= 20:
            step = 1
        elif width <= 50:
            step = 5
        elif width <= 100:
            step = 10
        elif width <= 200:
            step = 20
        elif width <= 500:
            step = 50
        else:
            step = 100

        axis.xaxis.set_major_locator(MultipleLocator(step))

    def _on_xlim_changed(self, axis):
        if self._is_clamping:
            return

        xmin, xmax = axis.get_xlim()
        width = xmax - xmin

        new_xmin = xmin
        new_xmax = xmax

        if new_xmin < 0:
            new_xmin = 0
            new_xmax = width

        if self._max_t > 0 and new_xmax > self._max_t:
            new_xmax = self._max_t
            new_xmin = self._max_t - width

            if new_xmin < 0:
                new_xmin = 0

        if new_xmin != xmin or new_xmax != xmax:
            self._is_clamping = True
            axis.set_xlim(new_xmin, new_xmax)
            self._is_clamping = False

        if self._fixed_ylim is not None:
            ymin, ymax = self._fixed_ylim
            current_ymin, current_ymax = axis.get_ylim()
            if (current_ymin, current_ymax) != (ymin, ymax):
                self._is_clamping = True
                axis.set_ylim(ymin, ymax)
                self._is_clamping = False

        self._canvas.draw_idle()

    def _on_ylim_changed(self, axis):
        if self._is_clamping or self._fixed_ylim is None:
            return

        ymin, ymax = self._fixed_ylim
        current_ymin, current_ymax = axis.get_ylim()

        if (current_ymin, current_ymax) != (ymin, ymax):
            self._is_clamping = True
            axis.set_ylim(ymin, ymax)
            self._is_clamping = False
            self._canvas.draw_idle()