#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: str_enums.py
Author: Jonas Bordewick
Date: 23.03.26
Contact: jonas.bordewick@uni-a.de
"""
from enum import Enum


class ValueMode(Enum):
    RAW = "raw"
    SECOND = "per_second"

class LogChartType(Enum):
    LINE = "line"
    BOX = "box"

class CompareMode(Enum):
    INDIVIDUAL = "individual"
    GROUP = "grouped"

class Aggregation(Enum):
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    SUM = "sum"