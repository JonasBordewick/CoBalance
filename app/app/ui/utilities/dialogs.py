#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: dialogs.py
Author: Jonas Bordewick
Date: 10.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QWidget

from app.models import Group
from app.viewmodels import LogsExplorerViewModel, LogsGroupViewModel


def create_group_from_selection_via_dialog(parent: QWidget, logs_explorer_view_model: LogsExplorerViewModel):
    dialog = QInputDialog(parent)
    dialog.setWindowTitle("Create Group")
    dialog.setLabelText("Group name:")
    dialog.resize(420, 120)

    if dialog.exec():
        name = dialog.textValue()
        try:
            logs_explorer_view_model.create_group_from_selection(name)
        except ValueError as e:
            QMessageBox.warning(parent, "Create Group", str(e))

def rename_group_via_dialog(parent: QWidget, logs_group_view_model: LogsGroupViewModel, group: Group):
    dialog = QInputDialog(parent)
    dialog.setWindowTitle("Rename Group")
    dialog.setLabelText("New group name:")
    dialog.setTextValue(group.name)

    dialog.resize(420, 120)

    if dialog.exec():
        name = dialog.textValue()

        try:
            logs_group_view_model.rename_group(group.id, name)
        except ValueError as e:
            QMessageBox.warning(parent, "Rename Group", str(e))