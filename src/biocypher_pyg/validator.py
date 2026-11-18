"""Structural validation for converted heterogeneous graphs."""

from __future__ import annotations


def validate_heterodata(data, metadata) -> list[str]:
    errors: list[str] = []

    for node_type in data.node_types:
        expected = len(metadata.node_ids.get(node_type, []))
        actual = int(data[node_type].num_nodes or 0)
        if expected != actual:
            errors.append(
                f"{node_type}: metadata has {expected} IDs but HeteroData "
                f"has {actual} nodes"
            )

    for edge_type in data.edge_types:
        store = data[edge_type]
        edge_index = store.edge_index
        if edge_index.ndim != 2 or edge_index.shape[0] != 2:
            errors.append(f"{edge_type}: edge_index must have shape [2, E]")
            continue

        src_type, _, dst_type = edge_type
        if edge_index.numel():
            if int(edge_index[0].min()) < 0:
                errors.append(f"{edge_type}: negative source index")
            if int(edge_index[1].min()) < 0:
                errors.append(f"{edge_type}: negative target index")
            if int(edge_index[0].max()) >= int(data[src_type].num_nodes):
                errors.append(f"{edge_type}: source index out of range")
            if int(edge_index[1].max()) >= int(data[dst_type].num_nodes):
                errors.append(f"{edge_type}: target index out of range")

        edge_metadata = metadata.edge_records.get(edge_type, [])
        if len(edge_metadata) != edge_index.shape[1]:
            errors.append(
                f"{edge_type}: {len(edge_metadata)} metadata records for "
                f"{edge_index.shape[1]} edges"
            )

    return errors
