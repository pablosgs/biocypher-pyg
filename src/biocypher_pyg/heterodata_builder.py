"""Build a PyG HeteroData object from normalized conversion products."""

from __future__ import annotations

from torch_geometric.data import HeteroData


def build_heterodata(grouped_nodes, grouped_edges, feature_config=None):
    data = HeteroData()
    feature_config = feature_config or {}

    for node_type, nodes in grouped_nodes.items():
        data[node_type].num_nodes = len(nodes)
        names = feature_config.get(node_type, [])
        if names:
            from .converters.features import encode_numeric_features
            data[node_type].x = encode_numeric_features(nodes, names)

    for edge_type, values in grouped_edges.items():
        data[edge_type].edge_index = values["edge_index"]

    return data
