#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_table_row.py
Author: Jonas Bordewick
Date: 08.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from dataclasses import dataclass

@dataclass
class Group:
    id: str
    name: str

    @staticmethod
    def from_dict(data: dict):
        return Group(
            id=data['id'],
            name=data['name'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
        }

@dataclass(frozen=True)
class LogsTableRow:
    file_name: str
    file_path: str
    timestamp: float