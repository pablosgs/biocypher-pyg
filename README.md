# biocypher-pyg

A research-oriented bridge from biomedical knowledge graph records to
[PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) heterogeneous graphs.

> **Status:** early scaffold.

## Scope of v0.1

- Convert normalized node and edge records into `torch_geometric.data.HeteroData`.
- Keep node identifiers in per-node-type, reversible mappings.
- Preserve original node/edge properties in a sidecar metadata object.
- Build typed `edge_index` stores and validate index bounds.
- Save/load graph plus metadata.

Out of scope for this initial scaffold: universal BioCypher backend support,
automatic ontology alignment, text embeddings, automatic categorical encoding,
and graph neural network training.

## Install

Python 3.10+ is required.

```bash
python -m venv .venv
source .venv/bin/activate         
python -m pip install -U pip
pip install -e ".[dev]"
```

Install a PyTorch build appropriate for your CPU/CUDA environment first if the
default dependency resolver is not suitable for your machine. See the official
PyTorch and PyG installation instructions.

## Quick start (normalized records)

```python
from biocypher_pyg import BioCypherToPyG, NodeRecord, EdgeRecord

nodes = [
    NodeRecord("HGNC:11998", "gene", {"symbol": "TP53"}),
    NodeRecord("UniProt:P04637", "protein", {"name": "p53"}),
    NodeRecord("MONDO:0007254", "disease", {"name": "Example disease"}),
]
edges = [
    EdgeRecord(
        source_id="HGNC:11998",
        target_id="UniProt:P04637",
        source_type="gene",
        target_type="protein",
        relation_type="encodes",
        properties={"source": "synthetic", "evidence": "curated"},
    ),
    EdgeRecord(
        source_id="UniProt:P04637",
        target_id="MONDO:0007254",
        source_type="protein",
        target_type="disease",
        relation_type="associated_with",
        properties={"score": 0.95},
    ),
]

result = BioCypherToPyG.from_records(nodes, edges).convert()
data = result.data

print(data.node_types)
print(data.edge_types)
print(data["gene", "encodes", "protein"].edge_index)
print(result.metadata.node_ids["gene"])
```

Run tests:

```bash
pytest
```

## Design principles

1. Biological IDs are not tensor indices. `NodeIdMapper` maintains per-type,
   reversible mappings.
2. Edge direction and relation triplets are explicit.
3. Original properties are preserved as metadata; tensor feature encoding is
   opt-in and deliberately conservative.
4. Duplicate edges are retained unless a future explicit policy says otherwise.
5. Input adapters normalize source-specific data before conversion.

## BioCypher integration

Implement a source-specific adapter that yields `NodeRecord` and `EdgeRecord`.
Do not assume that every BioCypher output backend exposes the same read API.
See [`docs/biocypher_integration.md`](docs/biocypher_integration.md).

## Repository status

This scaffold is not yet a validated release. Before publishing a public
release, select a project license, pin/test supported dependency versions,
implement at least one real BioCypher ingestion route, and document its limits.
