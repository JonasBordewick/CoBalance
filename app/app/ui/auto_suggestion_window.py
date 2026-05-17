#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: auto_suggestion_window.py
Author: Jonas Bordewick
Date: 30.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGroupBox, QFormLayout, QVBoxLayout, QLineEdit, QComboBox, QSpinBox, QHBoxLayout, \
    QPushButton, QScrollArea, QDoubleSpinBox, QMessageBox

from app.domain.auto_suggestion import ParameterSettings, AutoSuggestionSettings
from app.models import ParameterTableRow
from app.ui.widgets import ParameterSettingsListTile
from app.viewmodels import SettingsViewModel, project_context_view_model
from app.viewmodels.job_view_model import JobViewModel


class AutoSuggestionWindow(QWidget):
    def __init__(
            self,
            settings_view_model: SettingsViewModel,
            job_view_model: JobViewModel,
            parent=None
    ):
        super().__init__(parent)

        self._settings_view_model = settings_view_model
        self._job_view_model = job_view_model
        self._project_context_view_model = project_context_view_model

        self.setWindowTitle("Auto Suggestion")
        self.resize(420, 800)

        self._parameter_list_widgets: list[ParameterSettingsListTile] = []

        self._build_ui()
        self._job_view_model.selected_parameters_changed.connect(self.on_selection_changed)
        self._job_view_model.state_changed.connect(self.on_running_changed)

    def closeEvent(self, event):
        super().closeEvent(event)

    def refresh_ui(self):
        self._update_ui_from_view_model()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)

        self.context_group = QGroupBox("Context Settings")
        context_form = QFormLayout()
        context_form.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

        self._snapshot_identifier_edit = QLineEdit()
        self._snapshot_identifier_edit.setPlaceholderText("Enter Snapshot Identifier")
        self._snapshot_identifier_edit.setToolTip("An identifier for this optimization run. Used to name the output balance files and to distinguish results from different runs.")

        self.balance_combo = QComboBox()
        self.balance_combo.setToolTip("The balance file to use as a base for the auto-suggestion process.")
        self.scene_combo = QComboBox()
        self.scene_combo.setToolTip("The unity scene where the simulation will be executed.")

        context_form.addRow("Snapshot Identifier", self._snapshot_identifier_edit)
        context_form.addRow("Base Balance Snapshot", self.balance_combo)
        context_form.addRow("Unity Scene", self.scene_combo)
        self.context_group.setLayout(context_form)

        self.execution_group = QGroupBox("Execution Settings")
        execution_form = QFormLayout()
        execution_form.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

        self._method_combo = QComboBox()
        self._method_combo.addItem("Genetic Algorithm")
        self._method_combo.setToolTip("The optimization algorithm to use. Currently only Genetic Algorithm is supported.")

        self._population_size_spinbox = QSpinBox()
        self._population_size_spinbox.setMinimum(1)
        self._population_size_spinbox.setMaximum(10000)
        self._population_size_spinbox.setValue(50)
        self._population_size_spinbox.setToolTip("Number of candidate solutions in each generation.")

        self._num_generations_spinbox = QSpinBox()
        self._num_generations_spinbox.setMinimum(1)
        self._num_generations_spinbox.setMaximum(10000)
        self._num_generations_spinbox.setValue(20)
        self._num_generations_spinbox.setToolTip("Number of generations the algorithm runs. More generations allow deeper optimization but increase total runtime.")

        self._iterations_per_individual_spinbox = QSpinBox()
        self._iterations_per_individual_spinbox.setMinimum(1)
        self._iterations_per_individual_spinbox.setMaximum(10000)
        self._iterations_per_individual_spinbox.setValue(5)
        self._iterations_per_individual_spinbox.setToolTip("Number of iterations for each individual in the simulation to get an average performance estimate.")

        self._elite_count_spinbox = QSpinBox()
        self._elite_count_spinbox.setMinimum(1)
        self._elite_count_spinbox.setMaximum(10000)
        self._elite_count_spinbox.setValue(4)
        self._elite_count_spinbox.setToolTip("Number of top-performing individuals to keep as output. Each is saved as a separate balance file.")

        self._speed_multiplier_spinbox = QDoubleSpinBox()
        self._speed_multiplier_spinbox.setRange(1.0, 20.0)
        self._speed_multiplier_spinbox.setSingleStep(0.5)
        self._speed_multiplier_spinbox.setValue(1.0)
        self._speed_multiplier_spinbox.setToolTip("Speed multiplier for the simulation for each individual. (From 1 to 20)")

        self._max_simulation_time_spinbox = QSpinBox()
        self._max_simulation_time_spinbox.setRange(1, 10000)
        self._max_simulation_time_spinbox.setValue(60)
        self._max_simulation_time_spinbox.setToolTip("Maximum time for each simulation in seconds.")

        execution_form.addRow("Method", self._method_combo)
        execution_form.addRow("Population Size", self._population_size_spinbox)
        execution_form.addRow("Number of Generations", self._num_generations_spinbox)
        execution_form.addRow("Iterations per Individual", self._iterations_per_individual_spinbox)
        execution_form.addRow("Choose Top", self._elite_count_spinbox)
        execution_form.addRow("Speed Multiplier", self._speed_multiplier_spinbox)
        execution_form.addRow("Max Simulation Time [s]", self._max_simulation_time_spinbox)

        self.execution_group.setLayout(execution_form)

        self.parameter_group = QGroupBox("Parameter Settings")
        parameter_form = QVBoxLayout()

        parameters: list[ParameterTableRow] = self._job_view_model.selected_parameter_rows

        self.parameter_scroll = QScrollArea()
        self.parameter_scroll.setWidgetResizable(True)

        container = QWidget()
        self.parameter_list_layout = QVBoxLayout(container)
        self.parameter_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for parameter in parameters:
            row = ParameterSettingsListTile(parameter)
            self.parameter_list_layout.addWidget(row)
            self._parameter_list_widgets.append(row)

        self.parameter_scroll.setWidget(container)
        parameter_form.addWidget(self.parameter_scroll)

        self.parameter_group.setLayout(parameter_form)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton("Start Auto-Suggestion")
        self.start_button.setToolTip("Validate settings and start the genetic algorithm optimization.")
        self.start_button.setEnabled(not self._job_view_model.is_running)
        self.start_button.clicked.connect(self.on_clicked_start)
        button_layout.addWidget(self.start_button)

        root_layout.addWidget(self.context_group)
        root_layout.addWidget(self.execution_group)
        root_layout.addWidget(self.parameter_group, stretch=1)
        root_layout.addLayout(button_layout)

    def on_selection_changed(self):

        for widget in self._parameter_list_widgets:
            self.parameter_list_layout.removeWidget(widget)

        self._parameter_list_widgets = []

        parameters: list[ParameterTableRow] = self._job_view_model.selected_parameter_rows
        for parameter in parameters:
            row = ParameterSettingsListTile(parameter)
            self.parameter_list_layout.addWidget(row)
            self._parameter_list_widgets.append(row)

    def on_running_changed(self):
        self.start_button.setEnabled(not self._job_view_model.is_running)

    def on_clicked_start(self):
        identifier = self._snapshot_identifier_edit.text().strip()
        balance_name = self.balance_combo.currentText().strip()
        scene_name = self.scene_combo.currentText().strip()
        speed_multiplier = self._speed_multiplier_spinbox.value()
        max_simulation_time = self._max_simulation_time_spinbox.value()
        iterations_per_individual = self._iterations_per_individual_spinbox.value()
        population_size = self._population_size_spinbox.value()
        num_generations = self._num_generations_spinbox.value()
        elite_count = self._elite_count_spinbox.value()

        settings = []

        if not identifier:
            QMessageBox.warning(self, "Missing Identifier", "Please enter a simulation identifier.")
            return

        if not balance_name:
            QMessageBox.warning(self, "Missing Balance", "Please select a balance.")
            return

        if not scene_name:
            QMessageBox.warning(self, "Missing Scene", "Please select a scene.")
            return

        for widget in self._parameter_list_widgets:
            settings.append(widget.get_settings())

        auto_suggestion_setting = AutoSuggestionSettings(
            snapshot_id=identifier,
            population_size=population_size,
            generation_count=num_generations,
            elite_count=elite_count,
            runs_per_individual=iterations_per_individual,
            scene_path=self._settings_view_model.scenes.get(scene_name),
            base_balance_file_path=self._settings_view_model.balances.get(balance_name),
            time_scale=speed_multiplier,
            max_time=max_simulation_time,
            parameter_settings=settings
        )

        self.close()

        self._job_view_model.start_auto_suggestion(
            auto_suggestion_setting,
            self._settings_view_model.project_settings
        )


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

        self._speed_multiplier_spinbox.setValue(self._settings_view_model.app_settings.default_time_scale)
        self._max_simulation_time_spinbox.setValue(self._settings_view_model.app_settings.default_max_simulation_time)

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
