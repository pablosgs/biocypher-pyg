"""Node grouping and metadata preparation."""

from __future__ import annotations

from collections import defaultdict

from ..models import NodeRecord


def group_nodes(nodes: list[NodeRecord], schema_mapper):
    grouped = defaultdict(list)
    for node in nodes:
        pyg_type = schema_mapper.map_node_type(node.node_type)
        grouped[pyg_type].append(node)
    for node_type in grouped:
        grouped[node_type].sort(key=lambda item: item.node_id)
    return dict(grouped)
