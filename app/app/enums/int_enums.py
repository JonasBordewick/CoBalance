#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: int_enums.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from enum import IntEnum


class WatchType(IntEnum):
    DIRECTORY = 0
    FILE = 1

class ScreenType(IntEnum):
    PARAMETERS = 0
    COMPARISON = 1
    LOGS = 2

class ComparisonChartType(IntEnum):
    BAR = 0
    RADAR = 1