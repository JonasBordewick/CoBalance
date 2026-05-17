#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: selected_entity_table_row.py
Author: Jonas Bordewick
Date: 22.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass
from typing import Literal, Union

ParamType = Literal["int", "float"]
ParamValue = Union[int, float]

@dataclass(frozen=True)
class SelectedEntityParameterEntry:
    key: str
    display_name: str
    type: ParamType
    value: ParamValue | None

@dataclass(frozen=True)
class SelectedEntityTableData:
    entity_id: str
    display_name: str
    parameters: list[SelectedEntityParameterEntry]