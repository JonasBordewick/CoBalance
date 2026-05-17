#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: parsing.py
Author: Jonas Bordewick
Date: 11.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import json

import pandas as pd


# -------------------------
# Parsing log files
# -------------------------

def parse_log_file(file_path) -> dict[str, pd.DataFrame]:
    rows = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            t = obj.get("t", None)
            k = obj.get("k", None)
            if t is None or k is None:
                continue

            if "v" in obj:
                v = obj["v"]
            elif "f" in obj:
                v = obj["f"]
            elif "i" in obj:
                v = obj["i"]
            else:
                continue

            if not isinstance(v, (int, float)):
                continue

            rows.append((float(t), str(k), float(v)))

    df = pd.DataFrame(rows, columns=["t", "k", "v"])
    if df.empty:
        return {}

    df.sort_values(["k", "t"], inplace=True, kind="mergesort")
    df.reset_index(drop=True, inplace=True)

    log_by_key: dict[str, pd.DataFrame] = {}
    for key, group in df.groupby("k"):
        log_by_key[str(key)] = group[["t", "v"]].reset_index(drop=True)

    return log_by_key