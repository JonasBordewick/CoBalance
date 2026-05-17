#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: group_delegate.py
Author: Jonas Bordewick
Date: 10.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyledItemDelegate, QComboBox, QWidget, QCompleter
from PyQt6.QtCore import QTimer

from app.viewmodels import LogsGroupViewModel


class GroupDelegate(QStyledItemDelegate):
    def __init__(self, view_model: LogsGroupViewModel, parent: QWidget = None):
        super().__init__(parent=parent)
        self._vm = view_model

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setEditable(True)

        combo.addItem("")

        groups = sorted(g.name for g in self._vm.group_manager.groups_by_id.values())
        combo.addItems(groups)

        completer = QCompleter(groups, combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        combo.setCompleter(completer)

        #QTimer.singleShot(0, combo.showPopup)
        return combo

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.DisplayRole)
        if value is None:
            value = ""
        editor.setCurrentText(value)
        line_edit = editor.lineEdit()
        if line_edit is not None:
            line_edit.selectAll()

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.ItemDataRole.EditRole)