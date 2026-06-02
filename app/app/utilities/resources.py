#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: resources.py
Author: Jonas Bordewick
Date: 02.06.2026
Contact: jonas.bordewick@uni-a.de
"""
import os
import sys


def resource_path(relative_path: str) -> str:
    """Returns the absolute path — works in dev mode AND after PyInstaller build."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
