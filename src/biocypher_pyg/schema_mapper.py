"""Explicit mapping from source labels to PyG node/relation type names."""

from __future__ import annotations


class SchemaMapper:
    def __init__(
        self,
        node_types: dict[str, str] | None = None,
        relation_types: dict[str, str] | None = None,
    ) -> None:
        self.node_types = node_types or {}
        self.relation_types = relation_types or {}

    def map_node_type(self, source_type: str) -> str:
        return self.node_types.get(source_type, source_type.strip().lower())

    def map_relation_type(self, relation_type: str) -> str:
        return self.relation_types.get(relation_type, relation_type.strip().lower())
