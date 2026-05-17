#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: __init__.py
Author: Jonas Bordewick
Date: 10.03.2026
Contact: jonas.bordewick@uni-a.de
"""

from .dialogs import create_group_from_selection_via_dialog, rename_group_via_dialog
from .widget_builder import build_widget_and_layout

__all__ = [
    "create_group_from_selection_via_dialog",
    "rename_group_via_dialog",
    "build_widget_and_layout"
]


