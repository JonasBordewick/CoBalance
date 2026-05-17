#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: string_methods.py
Author: Jonas Bordewick
Date: 10.03.2026
Contact: jonas.bordewick@uni-a.de
"""


def normalize_group_name(name: str) -> str:
    return name.strip().casefold()
