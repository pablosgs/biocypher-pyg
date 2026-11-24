from biocypher_pyg import BioCypherToPyG, EdgeRecord, NodeRecord

nodes = [
    NodeRecord("HGNC:11998", "gene", {"symbol": "TP53", "score": 1.0}),
    NodeRecord("UniProt:P04637", "protein", {"name": "p53"}),
    NodeRecord("MONDO:0007254", "disease", {"name": "Example disease"}),
]
edges = [
    EdgeRecord(
        "HGNC:11998",
        "UniProt:P04637",
        "gene",
        "protein",
        "encodes",
        {"source": "synthetic", "evidence": "curated"},
    ),
    EdgeRecord(
        "UniProt:P04637",
        "MONDO:0007254",
        "protein",
        "disease",
        "associated_with",
        {"score": 0.95},
    ),
]

result = BioCypherToPyG.from_records(
    nodes,
    edges,
    feature_config={"gene": ["score"]},
).convert()

if not result.is_valid:
    raise RuntimeError(result.validation_errors)

print(result.data)
print("Node IDs:", result.metadata.node_ids)
print("Edge metadata:", result.metadata.edge_records)
