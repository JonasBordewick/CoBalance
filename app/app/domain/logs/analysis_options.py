#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: analysis_options.py
Author: Jonas Bordewick
Date: 23.03.26
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass

from app.enums import ValueMode, LogChartType, CompareMode, Aggregation


@dataclass
class AnalysisOptions:
    value_mode: ValueMode
    chart_type: LogChartType
    compare_mode: CompareMode
    aggregation: Aggregation
