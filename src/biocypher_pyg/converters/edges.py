"""Edge grouping and edge_index construction."""

from __future__ import annotations

from collections import defaultdict

import torch

from ..models import EdgeRecord


def group_edges(edges: list[EdgeRecord], schema_mapper, id_mapper):
    grouped = defaultdict(lambda: {"source": [], "target": [], "properties": []})

    for edge in edges:
        source_type = schema_mapper.map_node_type(edge.source_type)
        target_type = schema_mapper.map_node_type(edge.target_type)
        relation = schema_mapper.map_relation_type(edge.relation_type)
        edge_type = (source_type, relation, target_type)

        source_index = id_mapper.get_index(source_type, edge.source_id)
        target_index = id_mapper.get_index(target_type, edge.target_id)

        grouped[edge_type]["source"].append(source_index)
        grouped[edge_type]["target"].append(target_index)
        grouped[edge_type]["properties"].append(
            {
                "edge_id": edge.edge_id,
                **edge.properties,
            }
        )

    result = {}
    for edge_type, values in grouped.items():
        if values["source"]:
            edge_index = torch.tensor(
                [values["source"], values["target"]], dtype=torch.long
            )
        else:
            edge_index = torch.empty((2, 0), dtype=torch.long)
        result[edge_type] = {
            "edge_index": edge_index,
            "properties": values["properties"],
        }
    return result
