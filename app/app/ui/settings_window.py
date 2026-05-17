#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: settings_window.py
Author: Jonas Bordewick
Date: 17.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import math

from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QFormLayout, QComboBox, \
    QCheckBox, QSpinBox, QLineEdit, QHBoxLayout, QFileDialog, QDoubleSpinBox

from app.ui.utilities import build_widget_and_layout
from app.viewmodels import ProjectContextViewModel
from app.viewmodels.settings_view_model import SettingsViewModel


class SettingsWindow(QWidget):
    def __init__(
            self,
            settings_view_model: SettingsViewModel,
            project_context_view_model: ProjectContextViewModel,
            parent=None
    ):
        super().__init__(parent)

        self._settings_view_model = settings_view_model
        self._project_context_view_model = project_context_view_model
        self._themes = ["light", "dark"]

        self.setWindowTitle("Settings")
        self.resize(500, 300)

        self._build_ui()
        self._connect_signals()
        self._update_ui_from_vm()


    def _build_ui(self):
        root_layout = QVBoxLayout(self)

        # App Settings
        app_group = QGroupBox("App Settings")
        app_form = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self._themes)
        self.theme_combo.setToolTip("Switch between light and dark application theme.")

        self.auto_save_checkbox = QCheckBox("Enable auto save")
        self.auto_save_checkbox.setToolTip("Automatically save the balance file on every change. Disables the manual Save button.")

        self.runs_spinbox = QSpinBox()
        self.runs_spinbox.setRange(1, 1000)
        self.runs_spinbox.setValue(1)
        self.runs_spinbox.setToolTip("Default number of simulation runs pre-filled in the Simulation window.")

        self.time_scale_spinbox = QDoubleSpinBox()
        self.time_scale_spinbox.setRange(1.0, 20.0)
        self.time_scale_spinbox.setSingleStep(0.5)
        self.time_scale_spinbox.setValue(1.0)
        self.time_scale_spinbox.setToolTip("Default simulation speed multiplier pre-filled in the Simulation and Auto Suggestion windows. Higher values speed up the simulation but may reduce accuracy.")

        self.max_time_spinbox = QSpinBox()
        self.max_time_spinbox.setRange(1, 10000)
        self.max_time_spinbox.setValue(60)
        self.max_time_spinbox.setToolTip("Default maximum duration per simulation run in seconds. The simulation stops automatically when this limit is reached.")

        app_form.addRow("Theme", self.theme_combo)
        app_form.addRow("", self.auto_save_checkbox)
        app_form.addRow("Default Number of Runs", self.runs_spinbox)
        app_form.addRow("Default Speed Multiplier", self.time_scale_spinbox)
        app_form.addRow("Default Max Simulation Time [s]", self.max_time_spinbox)
        app_group.setLayout(app_form)

        # Project Settings
        has_project = self._settings_view_model.project_settings is not None

        project_group = QGroupBox("Project Settings")
        project_form = QFormLayout()

        self.log_tick_rate_spinbox = QSpinBox()
        self.log_tick_rate_spinbox.setRange(1, 100)
        self.log_tick_rate_spinbox.setEnabled(has_project)
        self.log_tick_rate_spinbox.setToolTip("How often (in seconds) the simulation writes a data point to the log file. Lower values give more detail but produce larger log files.")

        self.executable_path_edit = QLineEdit()
        self.executable_path_edit.setToolTip("Path to the Unity application executable used for running simulations.")
        self.executable_browse_button = QPushButton("Browse...")
        self.executable_browse_button.setToolTip("Browse for the Unity application executable.")

        executable_row = QWidget()
        executable_row_layout = QHBoxLayout(executable_row)
        executable_row_layout.setContentsMargins(0, 0, 0, 0)
        executable_row_layout.addWidget(self.executable_path_edit)
        executable_row_layout.addWidget(self.executable_browse_button)

        project_form.addRow("Logging Interval [s]", self.log_tick_rate_spinbox)
        project_form.addRow("Unity Executable", executable_row)
        project_group.setLayout(project_form)

        # Buttons
        button_layout = QHBoxLayout()
        self.close_button = QPushButton("Close")
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        root_layout.addWidget(app_group)
        root_layout.addWidget(project_group)
        root_layout.addStretch()
        root_layout.addLayout(button_layout)

    def _connect_signals(self):
        self.theme_combo.currentTextChanged.connect(self._settings_view_model.set_theme)
        self.auto_save_checkbox.toggled.connect(self._settings_view_model.set_auto_save)

        self.runs_spinbox.valueChanged.connect(self._settings_view_model.set_default_number_of_runs)
        self.time_scale_spinbox.valueChanged.connect(self._settings_view_model.set_default_time_scale)
        self.max_time_spinbox.valueChanged.connect(self._settings_view_model.set_default_max_simulation_time)

        self.log_tick_rate_spinbox.valueChanged.connect(self._settings_view_model.set_default_log_tick_rate)
        self.executable_path_edit.textChanged.connect(self._settings_view_model.set_unity_application_path)
        self.executable_browse_button.clicked.connect(self._on_browse_executable_clicked)

        self.close_button.clicked.connect(self.close)

    def refresh(self):
        self._update_ui_from_vm()

    def _update_ui_from_vm(self):
        app = self._settings_view_model.app_settings
        project = self._settings_view_model.project_settings

        theme_idx = 0
        for idx, theme in enumerate(self._themes):
            if theme == app.theme:
                theme_idx = idx
                break

        self.theme_combo.setCurrentIndex(theme_idx)
        self.auto_save_checkbox.setChecked(app.auto_save)
        self.time_scale_spinbox.setValue(app.default_time_scale)
        self.max_time_spinbox.setValue(app.default_max_simulation_time)
        self.runs_spinbox.setValue(app.default_number_of_runs)
        if project:
            self.log_tick_rate_spinbox.setEnabled(True)
            self.log_tick_rate_spinbox.setValue(math.floor(project.default_log_tick_rate * 0.02))

            self.executable_path_edit.setEnabled(True)
            self.executable_path_edit.blockSignals(True)
            self.executable_path_edit.setText(project.unity_application_path)
            self.executable_path_edit.blockSignals(False)
            self.executable_browse_button.setEnabled(True)

        else:
            self.log_tick_rate_spinbox.setEnabled(False)
            self.log_tick_rate_spinbox.clear()

            self.executable_path_edit.setText("")
            self.executable_path_edit.setEnabled(False)

            self.executable_browse_button.setEnabled(False)

    def closeEvent(self, event):
        self._settings_view_model.save()
        super().closeEvent(event)

    def _on_browse_executable_clicked(self):
        start_path = self.executable_path_edit.text().strip()
        start_dir = ""

        if not start_path:
            last = self._settings_view_model.project_settings
            if last and last.unity_application_path:
                start_path = last.unity_application_path

        if start_path:
            info = QFileInfo(start_path)
            start_dir = info.absolutePath() if info.exists() else info.path()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable",
            start_dir,
            "All Files (*)"
        )

        if not file_path:
            return

        self.executable_path_edit.setText(file_path)


