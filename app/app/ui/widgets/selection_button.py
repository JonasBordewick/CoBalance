#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import pyqtSignal, QPoint
from PyQt6.QtGui import QActionGroup, QAction
from PyQt6.QtWidgets import QToolButton, QMenu


class SelectionButton(QToolButton):

    selection_changed = pyqtSignal(str)

    def __init__(self, selection_options=None, selected_option=None, parent=None):
        super().__init__(parent)

        self.setProperty("class", "selectionButton")

        self._selection_options = selection_options or []

        if selected_option not in self._selection_options:
            selected_option = self._selection_options[0] if self._selection_options else None

        self._selected_option = selected_option

        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        if self._selected_option:
            self.setText(f"Selected Balance: {self._selected_option}")

        self._rebuild_menu()

    def set_options(self, options):
        self._selection_options = options
        self._rebuild_menu()

    def set_selected(self, option):
        if option not in self._selection_options:
            return

        self._selected_option = option
        self.setText(f"Selected Balance: {option}")
        self._rebuild_menu()
        self.selection_changed.emit(option)

    def set_items(self, options: dict[str, str], selected_option: str = None):
        self._selection_options = options
        if selected_option and selected_option in options:
            self._selected_option = selected_option
            self.setText(f"Selected Balance: {selected_option}")
            self.setVisible(True)
        else:
            self._selected_option = None
            self.setText("")
            self.setVisible(False)
        self._rebuild_menu()

    def _rebuild_menu(self):
        menu = QMenu(self)
        action_group = QActionGroup(self)
        action_group.setExclusive(True)

        for name in self._selection_options:
            if name == self._selected_option:
                continue

            action = QAction(name, self)
            action.triggered.connect(lambda checked=False, n=name: self.set_selected(n))

            menu.addAction(action)
            action_group.addAction(action)

        self.setMenu(menu)