#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: logs_analysis_service.py
Author: Jonas Bordewick
Date: 23.03.26
Contact: jonas.bordewick@uni-a.de
"""

from .analysis_options import AnalysisOptions

import pandas as pd

from ...enums import Aggregation, ValueMode

from ...models import Group


class LogsAnalysisService:

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------CHART BUILDER-----------------------------------------
    # -----------------------------------------------------------------------------------------------

    def build_individual_line_chart_data(
        self,
        parameters: list[str],
        logs: dict[str, dict[str, pd.DataFrame]],
        options: AnalysisOptions
    ) -> dict[str, list[tuple[str, pd.DataFrame]]]:

        result: dict[str, list[tuple[str, pd.DataFrame]]] = {}

        for parameter_key in parameters:
            series: list[tuple[str, pd.DataFrame]] = self._get_individual_series_for_key(parameter_key, logs, options)
            if series:
                result[parameter_key] = series

        return result

    def build_grouped_line_chart_data(
        self,
        parameters: list[str],
        logs: dict[str, dict[str, pd.DataFrame]],
        selected_groups: list[Group],
        group_id_by_log_name: dict[str, str],
        options: AnalysisOptions
    ) -> dict[str, list[tuple[str, pd.DataFrame]]]:

        result: dict[str, list[tuple[str, pd.DataFrame]]] = {}

        for parameter_key in parameters:
            grouped_series: list[tuple[str, pd.DataFrame]] = []
            for group in selected_groups:
                series = self._get_series_for_group_and_key(group, parameter_key, logs, group_id_by_log_name, options)
                data = self._get_aggregated_data_for_series(series, options)
                if not data.empty:
                    grouped_series.append((group.name, data))

            if grouped_series:
                result[parameter_key] = grouped_series

        return result

    def build_individual_boxplot_data(
        self,
        parameters: list[str],
        logs: dict[str, dict[str, pd.DataFrame]],
        options: AnalysisOptions
    ) -> dict[str, list[tuple[str, list[float]]]]:

        result: dict[str, list[tuple[str, list[float]]]] = {}

        for parameter_key in parameters:
            samples: list[tuple[str, list[float]]] = []
            series = self._get_individual_series_for_key(parameter_key, logs, options)

            for label, data in series:
                values = self._extract_values(data)
                if values:
                    samples.append((label, values))

            if samples:
                result[parameter_key] = samples

        return result

    def build_grouped_boxplot_data(
        self, parameters: list[str],
        logs: dict[str, dict[str, pd.DataFrame]],
        selected_groups: list[Group],
        group_id_by_log_name: dict[str, str],
        options: AnalysisOptions
    ) -> dict[str, list[tuple[str, list[float]]]]:
        result: dict[str, list[tuple[str, list[float]]]] = {}

        for parameter_key in parameters:
            grouped_samples: list[tuple[str, list[float]]] = []
            for group in selected_groups:
                series = self._get_series_for_group_and_key(group, parameter_key, logs,group_id_by_log_name, options)
                data = self._get_aggregated_data_for_series(series, options)
                values: list[float] = self._extract_values(data)
                if values:
                    grouped_samples.append((group.name, values))

            if grouped_samples:
                result[parameter_key] = grouped_samples

        return result



    def _transform_series_for_value_mode(self, data: pd.DataFrame, options: AnalysisOptions) -> pd.DataFrame:
        if data.empty:
            return pd.DataFrame(columns=["t", "v"])

        if options.value_mode == ValueMode.RAW:
            return data[["t", "v"]].copy()

        if options.value_mode == ValueMode.SECOND:
            return self._create_value_per_second(data)

        raise ValueError(f"Unknown value mode: {options.value_mode}")

    def _get_individual_series_for_key(
            self, parameter_key: str,
            logs: dict[str, dict[str, pd.DataFrame]],
            options: AnalysisOptions) -> list[tuple[str, pd.DataFrame]]:

        series: list[tuple[str, pd.DataFrame]] = []

        for log_name, by_key in logs.items():
            data = by_key.get(parameter_key)
            if data is None or data.empty:
                continue
            data = self._transform_series_for_value_mode(data, options)
            if data.empty:
                continue
            series.append((log_name, data))

        return series

    def _get_series_for_group_and_key(
            self, group: Group, parameter_key: str,
            logs: dict[str, dict[str, pd.DataFrame]],
            group_id_by_log_name: dict[str, str],
            options: AnalysisOptions) -> list[pd.DataFrame]:
        series: list[pd.DataFrame] = []

        for log_name, by_key in logs.items():

            if ((log_name not in group_id_by_log_name) or
                (group_id_by_log_name[log_name] != group.id)):
                continue

            data = self._transform_series_for_value_mode(by_key.get(parameter_key, None), options)
            if data is None or data.empty:
                continue

            series.append(data)

        return series

    # -----------------------------------------------------------------------------------------------
    # --------------------------------------------HELPER---------------------------------------------
    # -----------------------------------------------------------------------------------------------

    @staticmethod
    def _create_value_per_second(data: pd.DataFrame) -> pd.DataFrame:
        if data is None or data.empty:
            return pd.DataFrame(columns=["t", "v"])

        df = data[["t", "v"]].copy()
        dv = df["v"].diff()
        dt = df["t"].diff()

        df["v"] = dv / dt.replace(0, pd.NA)
        df = df.dropna(subset=["v"])
        return df[["t", "v"]].reset_index(drop=True)

    @staticmethod
    def _merge_series_on_time(series: list[pd.DataFrame]) -> pd.DataFrame:
        if not series:
            return pd.DataFrame(columns=["t", "v"])

        valid = [
            data[["t", "v"]].copy().rename(columns={"v": f"v_{idx}"}).set_index("t")
            for idx, data in enumerate(series)
            if data is not None and not data.empty
        ]

        if not valid:
            return pd.DataFrame(columns=["t", "v"])

        merged = pd.concat(valid, axis=1, join="outer").sort_index().reset_index().copy()

        if "index" in merged.columns:
            merged = merged.rename(columns={"index": "t"})

        return merged

    @staticmethod
    def _extract_values(data: pd.DataFrame) -> list[float]:
        if data is None or data.empty:
            return []

        return data["v"].dropna().tolist()


    # -----------------------------------------------------------------------------------------------
    # ------------------------------------------AGGREGATION------------------------------------------
    # -----------------------------------------------------------------------------------------------

    def _get_aggregated_data_for_series(self, series: list[pd.DataFrame], options: AnalysisOptions) -> pd.DataFrame:
        if options.aggregation == Aggregation.MEAN:
            return self._mean_series(series)
        if options.aggregation == Aggregation.MEDIAN:
            return self._median_series(series)
        if options.aggregation == Aggregation.MIN:
            return self._min_series(series)
        if options.aggregation == Aggregation.MAX:
            return self._max_series(series)
        if options.aggregation == Aggregation.SUM:
            return self._sum_series(series)
        raise ValueError(f"Unknown group aggregation: {options.aggregation}")

    def _mean_series(self, series: list[pd.DataFrame]) -> pd.DataFrame:
        merged = self._merge_series_on_time(series)
        if merged.empty:
            return merged
        value_columns = [col for col in merged.columns if col.startswith("v_")]
        merged = merged.copy()
        merged["v"] = merged[value_columns].mean(axis=1, skipna=True)
        return merged[["t", "v"]].reset_index(drop=True)

    def _median_series(self, series: list[pd.DataFrame]) -> pd.DataFrame:
        merged = self._merge_series_on_time(series)
        if merged.empty:
            return merged
        value_columns = [col for col in merged.columns if col.startswith("v_")]
        merged = merged.copy()
        merged["v"] = merged[value_columns].median(axis=1, skipna=True)
        return merged[["t", "v"]].reset_index(drop=True)

    def _min_series(self, series: list[pd.DataFrame]) -> pd.DataFrame:
        merged = self._merge_series_on_time(series)
        if merged.empty:
            return merged
        value_columns = [col for col in merged.columns if col.startswith("v_")]
        merged = merged.copy()
        merged["v"] = merged[value_columns].min(axis=1, skipna=True)
        return merged[["t", "v"]].reset_index(drop=True)

    def _max_series(self, series: list[pd.DataFrame]) -> pd.DataFrame:
        merged = self._merge_series_on_time(series)
        if merged.empty:
            return merged
        value_columns = [col for col in merged.columns if col.startswith("v_")]
        merged = merged.copy()
        merged["v"] = merged[value_columns].max(axis=1, skipna=True)
        return merged[["t", "v"]].reset_index(drop=True)

    def _sum_series(self, series: list[pd.DataFrame]) -> pd.DataFrame:
        merged = self._merge_series_on_time(series)
        if merged.empty:
            return merged
        value_columns = [col for col in merged.columns if col.startswith("v_")]
        merged = merged.copy()
        merged["v"] = merged[value_columns].sum(axis=1, skipna=True)
        return merged[["t", "v"]].reset_index(drop=True)