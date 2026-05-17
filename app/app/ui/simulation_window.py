#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: simulation_window.py
Author: Jonas Bordewick
Date: 21.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QHBoxLayout, QPushButton, QMessageBox, QDoubleSpinBox
)

from app.models.job_settings import JobSettings
from app.viewmodels import SettingsViewModel, ProjectContextViewModel


class SimulationWindow(QWidget):
    start_simulation_requested = pyqtSignal(JobSettings, int)

    def __init__(self, settings_view_model: SettingsViewModel, project_context_view_model: ProjectContextViewModel, parent=None):
        super().__init__(parent)

        self._settings_view_model = settings_view_model
        self._project_context_view_model = project_context_view_model

        self.setWindowTitle("Simulation Settings")
        self.resize(420, 240)

        self._build_ui()
        self._connect_signals()

    def closeEvent(self, event):
        super().closeEvent(event)

    def refresh_ui(self):
        self._update_ui_from_view_model()

    def set_running(self, is_running: bool):
        self.start_button.setEnabled(not is_running)

    def _build_ui(self):
        root_layout = QVBoxLayout(self)

        self.context_group = QGroupBox("Context Settings")
        context_form = QFormLayout()

        self.simulation_identifier_edit = QLineEdit()
        self.simulation_identifier_edit.setPlaceholderText("Enter simulation identifier")
        self.simulation_identifier_edit.setToolTip("Simulation identifier, determines the log file name and is used to group runs together. Should be unique for each set of runs.")

        self.balance_combo = QComboBox()
        self.balance_combo.setToolTip("Select the balance snapshot to use for the simulation runs.")
        self.scene_combo = QComboBox()
        self.scene_combo.setToolTip("The unity scene where the simulation will be executed.")

        context_form.addRow("Simulation Identifier", self.simulation_identifier_edit)
        context_form.addRow("Balancing Snapshot", self.balance_combo)
        context_form.addRow("Unity Scene", self.scene_combo)
        self.context_group.setLayout(context_form)

        self.execution_group = QGroupBox("Execution Settings")
        execution_form = QFormLayout()

        self.number_of_runs_spinbox = QSpinBox()
        self.number_of_runs_spinbox.setRange(1, 1000)
        self.number_of_runs_spinbox.setValue(1)
        self.number_of_runs_spinbox.setToolTip("How many times the simulation runs with the selected balance. Multiple runs average out random variation in the results.")

        self.speed_multiplier_spinbox = QDoubleSpinBox()
        self.speed_multiplier_spinbox.setRange(1.0, 20.0)
        self.speed_multiplier_spinbox.setSingleStep(0.5)
        self.speed_multiplier_spinbox.setValue(1.0)
        self.speed_multiplier_spinbox.setToolTip("Speed multiplier for the simulation. (From 1 to 20)")

        self.max_simulation_time_spinbox = QSpinBox()
        self.max_simulation_time_spinbox.setRange(1, 10000)
        self.max_simulation_time_spinbox.setValue(60)
        self.max_simulation_time_spinbox.setToolTip("Maximum time for each simulation in seconds.")

        execution_form.addRow("Number of Runs", self.number_of_runs_spinbox)
        execution_form.addRow("Speed Multiplier", self.speed_multiplier_spinbox)
        execution_form.addRow("Max Simulation Time [s]", self.max_simulation_time_spinbox)
        self.execution_group.setLayout(execution_form)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Simulations")
        self.start_button.setToolTip("Validate settings and start the simulation runs.")
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)

        root_layout.addWidget(self.context_group)
        root_layout.addWidget(self.execution_group)
        root_layout.addStretch()
        root_layout.addLayout(button_layout)

    def _connect_signals(self):
        self.start_button.clicked.connect(self._on_start_clicked)

    def _on_start_clicked(self):
        identifier = self.simulation_identifier_edit.text().strip()
        balance_name = self.balance_combo.currentText().strip()
        scene_name = self.scene_combo.currentText().strip()
        number_of_runs = self.number_of_runs_spinbox.value()
        speed_multiplier = self.speed_multiplier_spinbox.value()
        max_simulation_time = self.max_simulation_time_spinbox.value()

        if not identifier:
            QMessageBox.warning(self, "Missing Identifier", "Please enter a simulation identifier.")
            return

        if not balance_name:
            QMessageBox.warning(self, "Missing Balance", "Please select a balance.")
            return

        if not scene_name:
            QMessageBox.warning(self, "Missing Scene", "Please select a scene.")
            return

        job_settings = JobSettings(
            version="1.0",
            job_type="simulation",
            job_id=identifier,
            input_settings={
                "scenePath": self._settings_view_model.scenes.get(scene_name),
                "balanceFilePath": self._settings_view_model.balances.get(balance_name),
                "progressFilePath": self._project_context_view_model.progress_file_path,
                "iterations": number_of_runs,
            },
            execution_settings={
                "timeScale": speed_multiplier,
                "fixedDeltaTime": 0.02,
                "maxSimulationTime": max_simulation_time,
            }
        )

        self.close()
        self.start_simulation_requested.emit(job_settings, number_of_runs)

    def _update_ui_from_view_model(self):
        balances = list(self._settings_view_model.balances.keys())
        scenes = list(self._settings_view_model.scenes.keys())

        default_balance_file = self._settings_view_model.project_settings.default_balance_file
        balance_file_idx = 0

        for idx, balance_name in enumerate(balances):
            balance_path = self._settings_view_model.balances.get(balance_name)
            if balance_path == default_balance_file or balance_name == default_balance_file:
                balance_file_idx = idx
                break

        self.number_of_runs_spinbox.setValue(self._settings_view_model.app_settings.default_number_of_runs)
        self.speed_multiplier_spinbox.setValue(self._settings_view_model.app_settings.default_time_scale)
        self.max_simulation_time_spinbox.setValue(self._settings_view_model.app_settings.default_max_simulation_time)

        self.balance_combo.blockSignals(True)
        self.scene_combo.blockSignals(True)

        try:
            self.balance_combo.clear()
            self.balance_combo.addItems(balances)
            if balances:
                self.balance_combo.setCurrentIndex(balance_file_idx)

            self.scene_combo.clear()
            self.scene_combo.addItems(scenes)
        finally:
            self.balance_combo.blockSignals(False)
            self.scene_combo.blockSignals(False)