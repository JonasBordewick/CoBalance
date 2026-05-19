#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: main_window.py
Author: Jonas Bordewick
Date: 11.02.2026
Contact: jonas.bordewick@uni-a.de
"""
import webbrowser

from PyQt6.QtCore import Qt, QFileInfo, QUrl
from PyQt6.QtGui import QKeySequence, QDesktopServices
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QLabel

from app.enums import ScreenType
from app.models.job_settings import JobSettings
from app.ui.auto_suggestion_window import AutoSuggestionWindow
from app.ui.content_area import ContentArea
from app.ui.settings_window import SettingsWindow
from app.ui.simulation_window import SimulationWindow
from app.ui.utilities import create_group_from_selection_via_dialog
from app.ui.widgets import NavbarIconButton, HoverTooltip, NavbarIconButtonGroup, SelectionButton
from app.viewmodels import AppViewModel, BalanceViewModel, LogsExplorerViewModel, ProjectContextViewModel
from app.viewmodels.settings_view_model import SettingsViewModel
from app.viewmodels.job_view_model import JobViewModel


class MainWindow(QMainWindow):
    def __init__(self,
                 app_view_model: AppViewModel,
                 balance_view_model: BalanceViewModel,
                 logs_explorer_view_model: LogsExplorerViewModel,
                 settings_view_model: SettingsViewModel,
                 simulation_view_model: JobViewModel,
                 project_context_view_model: ProjectContextViewModel,
                 ):
        super().__init__()
        self.setWindowTitle("Balance Tool")
        self.resize(1200, 800)

        self.app_view_model = app_view_model
        self.balance_view_model = balance_view_model
        self.logs_explorer_view_model = logs_explorer_view_model
        self.logs_group_view_model = logs_explorer_view_model.logs_group_view_model
        self.settings_view_model = settings_view_model
        self.job_view_model = simulation_view_model
        self.project_context_view_model = project_context_view_model

        self.settings_window : SettingsWindow = SettingsWindow(
            settings_view_model=self.settings_view_model,
            project_context_view_model=self.project_context_view_model
        )
        self.simulation_window: SimulationWindow | None = None

        self.auto_suggestion_window: AutoSuggestionWindow | None = None

        self._setup_menubar()
        self._setup_ui()
        self._connect_signals()

    def _connect_signals(self):
        self.project_context_view_model.error_changed.connect(self._on_error)
        self.balance_view_model.load_state_changed.connect(self._on_load_state_changed)
        self.balance_view_model.balance_file_changed.connect(self._on_balance_file_changed)

        self.balance_view_model.file_loaded.connect(self._update_window_title)
        self.balance_view_model.dirty_changed.connect(self._update_window_title)
        self.logs_group_view_model.dirty_changed.connect(self._update_window_title)

        self.job_view_model.simulation_started.connect(self._on_simulation_started)
        self.job_view_model.auto_suggestion_started.connect(self._on_auto_suggestion_started)
        self.job_view_model.simulation_finished.connect(self._on_job_finished)
        self.job_view_model.auto_suggestion_progress.connect(self._on_auto_suggestion_progress)

        self.balance_view_model.external_file_changed.connect(self._on_external_change)

        self.project_context_view_model.available_balances_changed.connect(self._on_available_balances_changed)

        self.balance_selection.selection_changed.connect(
            self._on_balance_selection_changed,
        )

    def _on_error(self):
        latest_error = self.project_context_view_model.latest_error
        if not latest_error:
            return
        print(latest_error)

    def _on_load_state_changed(self):
        self.app_view_model.load_balance(self.balance_view_model.file)

    def _on_balance_file_changed(self):
        self.app_view_model.load_balance(self.balance_view_model.file)
        self.app_view_model.on_balance_file_changed(self.balance_view_model.file)


    def _on_available_balances_changed(self):
        self.balance_selection.set_items(
            self.project_context_view_model.available_balances,
            self.project_context_view_model.current_balance
        )
        self.balance_selection.setVisible(True)

    def _on_balance_selection_changed(self, balance_name: str):
        self.settings_view_model.set_default_balance_file(balance_name, save=True)


    def _setup_ui(self):
        self.central = QWidget()
        self.setCentralWidget(self.central)

        grid = QGridLayout(self.central)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        left_navbar = self._build_left_bar()
        right_navbar = self._build_right_bar()
        bottom_bar = self._build_bottom_bar()

        grid.addWidget(left_navbar, 0, 0)
        grid.addWidget(
            ContentArea(
                self.project_context_view_model,
                self.app_view_model,
                self.balance_view_model,
                self.logs_explorer_view_model,
                self.job_view_model
            ),
            0, 1)
        grid.addWidget(right_navbar, 0, 2)
        grid.addWidget(bottom_bar, 1, 0, 1, 3)

        grid.setColumnMinimumWidth(0, 40)
        grid.setColumnStretch(1, 1)
        grid.setColumnMinimumWidth(2, 40)

        grid.setRowStretch(0, 1)
        grid.setRowMinimumHeight(1, 30)

        self.central.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.central.setProperty("class", "main-window")

    def _build_left_bar(self) -> QWidget:
        button_group = NavbarIconButtonGroup()

        btn_overview = NavbarIconButton("❌", tooltip=HoverTooltip(text="Parameter Overview — Browse and edit all parameters of the loaded balance file."))
        btn_overview.clicked.connect(self._on_overview_button_clicked)
        btn_overview.setProperty("active", "true")
        btn_compare = NavbarIconButton("❌", tooltip=HoverTooltip(text="Entity Comparison — Compare parameter values across multiple entities side by side."))
        btn_compare.clicked.connect(self._on_comparison_button_clicked)
        btn_logs = NavbarIconButton("❌", tooltip=HoverTooltip(text="Logs — Explore and analyze simulation log files."))
        btn_logs.clicked.connect(self._on_logs_button_clicked)

        button_group.add(btn_overview)
        button_group.add(btn_compare)
        button_group.add(btn_logs)

        return self._build_navbar(button_group.buttons)

    def _build_right_bar(self):
        btn_simulation = NavbarIconButton(
            "❌",
            tooltip=HoverTooltip(text="Simulation — Configure and launch simulation runs with the current balance."),
            alignment=Qt.AlignmentFlag.AlignRight
        )
        btn_simulation.clicked.connect(self._on_simulation_button_clicked)

        btn_suggestion = NavbarIconButton(
            "❌",
            tooltip=HoverTooltip(text="Auto Suggestion — Run the genetic algorithm to find optimized balance parameters automatically."),
            alignment=Qt.AlignmentFlag.AlignRight
        )
        btn_suggestion.clicked.connect(self._on_suggestion_button_clicked)

        btn_group = NavbarIconButtonGroup()
        btn_group.add(btn_simulation)
        btn_group.add(btn_suggestion)

        return self._build_navbar(
            btn_group.buttons,
        )

    def _build_bottom_bar(self):
        widget = QWidget(self)
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        widget.setProperty("class", "navbar")

        widget.setFixedHeight(30)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(50, 0, 45, 2)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        layout.addSpacing(10)

        self.balance_selection = SelectionButton()
        self.balance_selection.setVisible(False)
        self.balance_selection.setToolTip("The currently active balance snapshot. Click to switch between available snapshots.")
        layout.addWidget(self.balance_selection)

        return widget

    def _build_navbar(self, widgets: list[QWidget], orientation: Qt.Orientation = Qt.Orientation.Vertical) -> QWidget:
        widget = QWidget(self)
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        widget.setProperty("class", "navbar")


        if orientation == Qt.Orientation.Vertical:
            widget.setFixedWidth(40)
            layout = QVBoxLayout()
            layout.setContentsMargins(6, 10, 6, 10)
        else:
            widget.setFixedHeight(30)
            layout = QHBoxLayout()
            layout.setContentsMargins(50, 0, 50, 2)

        layout.setSpacing(10)

        widget.setLayout(layout)

        for btn in widgets:
            layout.addWidget(btn)

        layout.addStretch()

        return widget


    def _setup_menubar(self):
        self.menuBar().setNativeMenuBar(True)
        # Project Menu
        project_menu = self.menuBar().addMenu("Project")
        action_open = project_menu.addAction("Open", QKeySequence("Ctrl+O"))
        action_open.triggered.connect(self._on_action_open_triggered)
        self.action_save = project_menu.addAction("Save", QKeySequence("Ctrl+S"))
        self.action_save.triggered.connect(self._on_action_save_triggered)

        self.action_save_as = project_menu.addAction("Save Balance as", QKeySequence("Ctrl+Shift+S"))
        self.action_save_as.triggered.connect(self._on_action_save_as_triggered)
        self.action_save_as.setEnabled(False)

        project_menu.addSeparator()
        action_settings = project_menu.addAction("Settings")
        action_settings.triggered.connect(self._on_action_settings_triggered)
        project_menu.addSeparator()
        action_exit = project_menu.addAction("Exit", QKeySequence("Ctrl+Q"))
        action_exit.triggered.connect(self.close)

        self.action_save.setEnabled(False)
        self.balance_view_model.load_state_changed.connect(lambda: self.update())
        self.balance_view_model.load_state_changed.connect(self._on_loaded_changed)
        self.balance_view_model.dirty_changed.connect(lambda: self._on_dirt_changed())
        self.logs_group_view_model.dirty_changed.connect(lambda: self._on_dirt_changed())

        self.settings_view_model.settings_changed.connect(self._on_settings_changed)

        # Selection Menu
        selection_menu = self.menuBar().addMenu("Selection")
        self.action_group_selection = selection_menu.addAction("Create Group From Selection", QKeySequence("Ctrl+G"))
        self.action_group_selection.setEnabled(False)
        self.action_group_selection.triggered.connect(self._on_action_group_selection_triggered)
        self.logs_explorer_view_model.log_selection_changed.connect(self._toggle_log_actions)

        self.action_remove_logs_from_group = selection_menu.addAction("Remove Selected Logs From Group")
        self.action_remove_logs_from_group.setEnabled(False)
        self.action_remove_logs_from_group.triggered.connect(self._on_action_remove_logs_from_group_triggered)
        self.logs_explorer_view_model.log_selection_changed.connect(self._toggle_log_actions)
        self.project_context_view_model.screen_changed.connect(lambda: self._toggle_log_actions())


        # Help Menu
        help_menu = self.menuBar().addMenu("Help")
        action_about = help_menu.addAction("About")
        action_about.triggered.connect(self._on_action_about_triggered)
        action_documentation = help_menu.addAction("Documentation")
        action_documentation.triggered.connect(self._on_action_documentation_triggered)


    def closeEvent(self, event):
        confirm = self.confirm_exit()

        if not confirm:
            event.ignore()
            return
        if self.settings_window:
            self.settings_window.close()
        if self.simulation_window:
            self.simulation_window.close()
        if self.auto_suggestion_window:
            self.auto_suggestion_window.close()

        super().closeEvent(event)


    # Action Handlers
    def _on_action_open_triggered(self):
        dialog = QFileDialog(self)

        if self.settings_view_model.app_settings.last_opened_file:
            last = self.settings_view_model.app_settings.last_opened_file
            if last:
                info = QFileInfo(last)
                dialog.setDirectory(info.absolutePath())
                dialog.selectFile(info.fileName())

        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Project Files (*.bfproject)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            if file_path:
                self.project_context_view_model.open_project(file_path)
            print(f"Selected file: {file_path}")

    def _on_action_save_triggered(self):
        if not self.balance_view_model.is_loaded:
            return
        self.balance_view_model.save_to_path(self.settings_view_model.get_default_balance_file_path())
        self.logs_group_view_model.save_to_file()

    def _on_action_save_as_triggered(self):
        if not self.balance_view_model.is_loaded:
            return

        start_path = self.settings_view_model.get_default_balance_file_path()

        if not start_path:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Balance As",
            start_path,
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".json"):
            file_path += ".json"

        self.balance_view_model.save_to_path(
            file_path
        )

    def _on_action_settings_triggered(self):
        if not self.settings_window:
            self.settings_window = SettingsWindow(
                settings_view_model=self.settings_view_model,
                project_context_view_model=self.project_context_view_model
            )
        self.settings_window.refresh()
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def _on_action_exit_triggered(self):
        self.close()

    def _on_action_about_triggered(self):
        print("About action triggered")

    def _on_action_documentation_triggered(self):
        QDesktopServices.openUrl(QUrl("https://cobalance.bordewick.dev"))

    def _on_action_group_selection_triggered(self):
        create_group_from_selection_via_dialog(self, self.logs_explorer_view_model)

    def _on_action_remove_logs_from_group_triggered(self):
        self.logs_explorer_view_model.remove_selected_logs_from_groups()

    # Action Togglers

    def _on_dirt_changed(self):
        if self.balance_view_model.is_loaded and self.settings_view_model.app_settings.auto_save:
            self.balance_view_model.save_to_path(self.settings_view_model.get_default_balance_file_path(), emit=False)
            self.logs_group_view_model.save_to_file(emit=False)
            return

        self.action_save.setEnabled(
            self.balance_view_model.is_loaded and
            (
                self.balance_view_model.is_dirty or
                self.logs_group_view_model.is_dirty
            )
        )

    def _on_settings_changed(self):
        if not self.balance_view_model.is_loaded:
            return
        self.balance_view_model.reload_from_path()

    def _on_loaded_changed(self):
        self.action_save_as.setEnabled(
            self.balance_view_model.is_loaded
        )

    def _toggle_log_actions(self):
        should_be_enabled = (
                self.logs_explorer_view_model.count_of_selected_logs > 0 and
                self.project_context_view_model.current_screen == ScreenType.LOGS
        )

        self.action_group_selection.setEnabled(should_be_enabled)
        self.action_remove_logs_from_group.setEnabled(should_be_enabled)

    # Button Handlers
    def _on_overview_button_clicked(self):
        self.project_context_view_model.set_screen(ScreenType.PARAMETERS)

    def _on_comparison_button_clicked(self):
        self.project_context_view_model.set_screen(ScreenType.COMPARISON)

    def _on_logs_button_clicked(self):
        self.project_context_view_model.set_screen(ScreenType.LOGS)

    def _on_simulation_button_clicked(self):
        if self.settings_view_model.project_settings is None:
            return

        if not self.simulation_window:
            self.simulation_window = SimulationWindow(self.settings_view_model, self.project_context_view_model)
            self.simulation_window.start_simulation_requested.connect(
                self._on_start_simulation_requested
            )

        self.simulation_window.refresh_ui()

        main_geom = self.frameGeometry()
        x = main_geom.right() + 8
        y = main_geom.top()

        self.simulation_window.move(x, y)
        self.simulation_window.show()
        self.simulation_window.raise_()
        self.simulation_window.activateWindow()

    def _on_suggestion_button_clicked(self):
        if self.settings_view_model.project_settings is None:
            return

        if not self.auto_suggestion_window:
            self.auto_suggestion_window = AutoSuggestionWindow(
                settings_view_model=self.settings_view_model,
                job_view_model=self.job_view_model
            )

        self.auto_suggestion_window.refresh_ui()

        main_geom = self.frameGeometry()
        x = main_geom.right() + 8
        y = main_geom.top()

        self.auto_suggestion_window.move(x, y)
        self.auto_suggestion_window.show()
        self.auto_suggestion_window.raise_()
        self.auto_suggestion_window.activateWindow()

    # Signal Handler
    def _on_start_simulation_requested(self, settings: JobSettings, runs: int):
        project_settings = self.settings_view_model.project_settings
        if project_settings is None:
            return

        self.job_view_model.start_simulation(
            project_settings=project_settings,
            job_settings=settings,
        )

    def _on_simulation_started(self):
        self.status_label.setText("Simulation running...")

    def _on_auto_suggestion_started(self):
        self.status_label.setText("Auto Suggestion running...")

    def _on_job_finished(self):
        self.status_label.setText("")

    def _on_auto_suggestion_progress(self, current_generation: int, total_generations: int):
        self.status_label.setText(f"Auto Suggestion: Generation {current_generation} / {total_generations}")

    # Window Title Handler
    def _update_window_title(self):
        title = "Balance Tool"
        if self.balance_view_model.is_loaded:
            title += f" - {self.project_context_view_model.current_project_name} - {self.project_context_view_model.current_balance}"
            if self.balance_view_model.is_dirty or self.logs_group_view_model.is_dirty:
                title += " *"
        self.setWindowTitle(title)

    def _on_external_change(self):
        confirm = self.confirm_reload_on_external_change()
        if confirm:
            print("Discard my changes")
            self.balance_view_model.reload_from_path()
            self.app_view_model.load_balance(self.balance_view_model.file)

        else:
            print("Ignore external change")

    # Confirm Exit if there are unsaved changes
    def confirm_exit(self) -> bool:
        if self.balance_view_model.is_dirty or self.logs_group_view_model.is_dirty:
            from PyQt6.QtWidgets import QMessageBox
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you really want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            return result == QMessageBox.StandardButton.Yes
        return True

    def confirm_reload_on_external_change(self) -> bool:
        if self.balance_view_model.is_dirty:
            from PyQt6.QtWidgets import QMessageBox
            result = QMessageBox.question(
                self,
                "External Change Detected",
                "The file has been changed on disk, but you have unsaved changes. Do you want to reload the file and lose your unsaved changes?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            return result == QMessageBox.StandardButton.Yes
        return True