#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: parameter_table_row.py
Author: Jonas Bordewick
Date: 16.02.2026
Contact: jonas.bordewick@uni-a.de
"""

from dataclasses import dataclass
from typing import Literal, Union

ParamType = Literal["int", "float"]
ParamValue = Union[int, float]

@dataclass(frozen=True)
class ParameterTableRow:
    key: str
    display_name: str
    type: ParamType
    value: ParamValue | None

    entity_id: str
    entity_name: str
    category: str
    tags: list[str]

