#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: entity_table_row.py
Author: Jonas Bordewick
Date: 21.02.2026
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class EntityTableRow:
    entity_id: str
    display_name: str
    category: str