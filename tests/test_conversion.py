import torch

from biocypher_pyg import BioCypherToPyG, EdgeRecord, NodeRecord


def example_records():
    nodes = [
        NodeRecord("HGNC:2", "gene", {"symbol": "B", "score": 2.0}),
        NodeRecord("HGNC:1", "gene", {"symbol": "A", "score": 1.0}),
        NodeRecord("UP:P1", "protein", {"name": "P1"}),
        NodeRecord("MONDO:1", "disease", {"name": "D1"}),
    ]
    edges = [
        EdgeRecord("HGNC:1", "UP:P1", "gene", "protein", "encodes", {"source": "test"}),
        EdgeRecord(
            "UP:P1", "MONDO:1", "protein", "disease", "associated_with", {"score": 0.8}
        ),
    ]
    return nodes, edges


def test_conversion_builds_heterodata():
    nodes, edges = example_records()
    result = BioCypherToPyG.from_records(nodes, edges).convert()

    assert result.is_valid, result.validation_errors
    assert set(result.data.node_types) == {"gene", "protein", "disease"}
    assert ("gene", "encodes", "protein") in result.data.edge_types
    assert result.data["gene", "encodes", "protein"].edge_index.shape == (2, 1)
    assert result.id_mapper.get_index("gene", "HGNC:1") == 0
    assert result.id_mapper.get_original_id("gene", 0) == "HGNC:1"


def test_numeric_features_are_opt_in():
    nodes, edges = example_records()
    result = BioCypherToPyG.from_records(
        nodes, edges, feature_config={"gene": ["score"]}
    ).convert()
    assert torch.equal(result.data["gene"].x, torch.tensor([[1.0], [2.0]]))


def test_missing_edge_endpoint_fails():
    nodes, edges = example_records()
    edges.append(EdgeRecord("HGNC:MISSING", "UP:P1", "gene", "protein", "encodes"))
    try:
        BioCypherToPyG.from_records(nodes, edges).convert()
    except KeyError:
        pass
    else:
        raise AssertionError("Expected unknown endpoint to raise KeyError")
