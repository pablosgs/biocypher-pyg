"""Opt-in numeric feature encoding.

Original properties remain in GraphMetadata. This deliberately small first
version encodes only explicitly selected, fully numeric properties.
"""

from __future__ import annotations

import math

import torch


def encode_numeric_features(nodes, feature_names: list[str]):
    if not feature_names:
        return None
    rows = []
    for node in nodes:
        row = []
        for name in feature_names:
            value = node.properties.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"Feature {name!r} must be numeric and present for every "
                    f"node; got {value!r} on {node.node_id!r}"
                )
            if not math.isfinite(float(value)):
                raise ValueError(f"Feature {name!r} must be finite")
            row.append(float(value))
        rows.append(row)
    return torch.tensor(rows, dtype=torch.float)
