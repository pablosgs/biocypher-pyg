"""Source-independent normalized records and conversion metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class NodeRecord:
    """A node in a normalized input graph."""

    node_id: str
    node_type: str
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.node_id, str) or not self.node_id.strip():
            raise ValueError("node_id must be a non-empty string")
        if not isinstance(self.node_type, str) or not self.node_type.strip():
            raise ValueError("node_type must be a non-empty string")
        if not isinstance(self.properties, dict):
            raise TypeError("properties must be a dictionary")


@dataclass(frozen=True, slots=True)
class EdgeRecord:
    """A directed edge with explicit endpoint types."""

    source_id: str
    target_id: str
    source_type: str
    target_type: str
    relation_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    edge_id: str | None = None

    def __post_init__(self) -> None:
        for name in ("source_id", "target_id", "source_type",
                     "target_type", "relation_type"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.properties, dict):
            raise TypeError("properties must be a dictionary")


@dataclass(slots=True)
class GraphMetadata:
    """Sidecar metadata that should not be forced into numeric tensors."""

    node_ids: dict[str, list[str]] = field(default_factory=dict)
    node_properties: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    edge_records: dict[tuple[str, str, str], list[dict[str, Any]]] = field(
        default_factory=dict
    )
    schema_mapping: dict[str, str] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    conversion_config: dict[str, Any] = field(default_factory=dict)
