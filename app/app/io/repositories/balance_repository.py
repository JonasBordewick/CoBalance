#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: balance_repository.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from app.models import BalanceFile


class BalanceRepository:

    @staticmethod
    def load_balance_from_file(file_path: str) -> BalanceFile | None:
        try:
            with open(file_path, 'r') as file:
                json_str = file.read()
                return BalanceFile.from_json(json_str)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_balance_to_file(balance_dto: BalanceFile, file_path: str):
        json_str = balance_dto.to_json()
        with open(file_path, 'w') as file:
            file.write(json_str)