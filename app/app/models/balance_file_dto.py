#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: balance_file_dto.py
Author: Jonas Bordewick
Date: 10.02.2026
Contact: jonas.bordewick@uni-a.de
"""

import json
from dataclasses import dataclass, field
from typing import Union, Literal

from app.models.entity_table_row import EntityTableRow
from app.models.parameter_table_row import ParameterTableRow
from app.models.selected_entity_table_row import SelectedEntityTableData, SelectedEntityParameterEntry

ParamType = Literal["int", "float"]
ParamValue = Union[int, float]

@dataclass
class ParameterDefinition:
    key: str
    display_name: str
    type: ParamType
    tags: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> 'ParameterDefinition':
        return ParameterDefinition(
            key=data['key'],
            display_name=data['displayName'],
            type=data['type'],
            tags=data.get('tags', [])
        )

    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'displayName': self.display_name,
            'type': self.type,
            'tags': self.tags
        }


@dataclass
class EntityDefinition:
    key: str
    display_name: str
    description: str = ""
    parameters: list[ParameterDefinition] = field(default_factory=list)
    category: str = ""

    @staticmethod
    def from_dict(data: dict) -> 'EntityDefinition':
        parameters = [ParameterDefinition.from_dict(param) for param in data.get('parameters', [])]
        return EntityDefinition(
            key=data['entityID'],
            display_name=data['displayName'],
            description=data.get('description', ""),
            parameters=parameters,
            category=data.get('category', ""),
        )

    def to_dict(self) -> dict:
        return {
            'entityID': self.key,
            'displayName': self.display_name,
            'description': self.description,
            'parameters': [param.to_dict() for param in self.parameters],
            'category': self.category
        }


@dataclass
class BalanceFile:
    schema_version: int
    entities: list[EntityDefinition] = field(default_factory=list)
    values: dict[str, ParamValue] = field(default_factory=dict)

    @staticmethod
    def from_json(json_str: str) -> 'BalanceFile':
        data = json.loads(json_str)
        entities = [EntityDefinition.from_dict(entity) for entity in data.get('entities', [])]
        values = {}
        for value in data.get('values', []):
            key = value['id']
            val = value['value']
            values[key] = val
        return BalanceFile(
            schema_version=data['schemaVersion'],
            entities=entities,
            values=values
        )

    def to_json(self) -> str:
        return json.dumps({
            'schemaVersion': self.schema_version,
            'entities': [entity.to_dict() for entity in self.entities],
            'values': [{'id': key, 'value': value} for key, value in self.values.items()]
        }, indent=4)

    def has_diff(self, other: 'BalanceFile') -> bool:
        if self.schema_version != other.schema_version:
            return True
        if len(self.entities) != len(other.entities):
            return True
        if len(self.values) != len(other.values):
            return True
        for e1, e2 in zip(self.entities, other.entities):
            if e1.key != e2.key:
                return True
            if e1.display_name != e2.display_name:
                return True
            if e1.category != e2.category:
                return True
            for p1, p2 in zip(e1.parameters, e2.parameters):
                if p1.key != p2.key:
                    return True
                if p1.display_name != p2.display_name:
                    return True
                if p1.type != p2.type:
                    return True
        for key in self.values.keys():
            if self.values[key] != other.values[key]:
                return True
        return False


    def build_parameter_rows(self) -> list[ParameterTableRow]:
        rows: list[ParameterTableRow] = []

        for entity in self.entities:
            for param in entity.parameters:
                value = self.values.get(f"{param.key}")
                row = ParameterTableRow(
                    key=f"{param.key}",
                    display_name=param.display_name,
                    type=param.type,
                    value=value,
                    entity_id=entity.key,
                    entity_name=entity.display_name,
                    category=entity.category,
                    tags=param.tags
                )
                rows.append(row)

        return rows

    def build_entity_rows(self) -> list[EntityTableRow]:
        rows: list[EntityTableRow] = []
        for entity in self.entities:
            row = EntityTableRow(
                entity_id=entity.key,
                display_name=entity.display_name,
                category=entity.category
            )
            rows.append(row)
        return rows

    def build_selected_entity_table_row(self, entity_id: str) -> Union[SelectedEntityTableData, None]:
        entity = next((e for e in self.entities if e.key == entity_id), None)
        if not entity:
            return None

        parameters = []
        for param in entity.parameters:
            value = self.values.get(f"{param.key}")
            param_entry = SelectedEntityParameterEntry(
                key=param.key,
                display_name=param.display_name,
                type=param.type,
                value=value
            )
            parameters.append(param_entry)

        return SelectedEntityTableData(
            entity_id=entity.key,
            display_name=entity.display_name,
            parameters=parameters
        )

