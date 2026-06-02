#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: main.py
Author: Jonas Bordewick
Date: 30.01.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

from app.ui import MainWindow
from app.viewmodels import AppViewModel, BalanceViewModel, LogsGroupViewModel, LogsExplorerViewModel, \
    ProjectContextViewModel
from app.utilities import resource_path

import sys
import traceback
import logging

from app.viewmodels.settings_view_model import SettingsViewModel
from app.viewmodels.job_view_model import JobViewModel

log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)

def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message.
    If unavailable (non-console application), log an additional notice.
    """
    if QtWidgets.QApplication.instance() is not None:
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText("Oops. An unexpected error occured:\n{0}".format(log_msg))
            errorbox.exec()
    else:
        log.debug("No QApplication instance available.")

class UncaughtHook(QtCore.QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
            log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)

qt_exception_hook = UncaughtHook()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Helle Palette erzwingen
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)
    with open(resource_path("styles/default.qss"), "r") as f:
        app.setStyleSheet(f.read())

    from app.io.watchers import DirectoryWatcherService
    directory_watcher_service = DirectoryWatcherService()

    # Create View Models
    project_context_view_model = ProjectContextViewModel(
        file_watcher=directory_watcher_service,
    )

    balance_view_model = BalanceViewModel(
        file_watcher=directory_watcher_service,
        project_context_view_model=project_context_view_model,
    )
    settings_view_model = SettingsViewModel(
        project_context_view_model=project_context_view_model,
    )
    simulation_view_model = JobViewModel(
        project_context_view_model=project_context_view_model,
        file_watcher=directory_watcher_service,
    )
    app_view_model = AppViewModel(
        project_context_view_model=project_context_view_model,
    )

    logs_group_view_mode = LogsGroupViewModel()
    logs_explorer_view_model = LogsExplorerViewModel(
        file_watcher=directory_watcher_service,
        logs_group_view_model=logs_group_view_mode,
        project_context_view_model=project_context_view_model,
    )

    window = MainWindow(
        app_view_model=app_view_model,
        balance_view_model=balance_view_model,
        logs_explorer_view_model=logs_explorer_view_model,
        settings_view_model=settings_view_model,
        simulation_view_model=simulation_view_model,
        project_context_view_model=project_context_view_model,
    )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()