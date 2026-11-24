"""Persistence helpers for conversion results."""

from __future__ import annotations

import json
from pathlib import Path

import torch

from .id_mapper import NodeIdMapper


def save_result(result, directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    # PyTorch serialization is pickle-based: only load files you trust.
    torch.save(result.data, directory / "graph.pt")

    metadata = {
        "node_ids": result.metadata.node_ids,
        "node_properties": result.metadata.node_properties,
        "edge_records": [
            {
                "edge_type": list(edge_type),
                "records": records,
            }
            for edge_type, records in result.metadata.edge_records.items()
        ],
        "schema_mapping": result.metadata.schema_mapping,
        "provenance": result.metadata.provenance,
        "conversion_config": result.metadata.conversion_config,
        "id_mapping": result.id_mapper.as_dict(),
    }
    (directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def load_graph(directory: str | Path, *, trusted: bool = False):
    if not trusted:
        raise ValueError(
            "PyTorch graph files use pickle-based serialization. "
            "Set trusted=True only for files from a trusted source."
        )
    directory = Path(directory)
    data = torch.load(directory / "graph.pt", map_location="cpu", weights_only=False)
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    mapper = NodeIdMapper.from_dict(metadata["id_mapping"])
    return data, metadata, mapper
