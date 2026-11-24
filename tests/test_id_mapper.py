import pytest

from biocypher_pyg import BioCypherToPyG
from biocypher_pyg.id_mapper import NodeIdMapper
from biocypher_pyg.models import NodeRecord


def test_mapping_is_deterministic_and_type_scoped():
    nodes = [
        NodeRecord("HGNC:2", "gene"),
        NodeRecord("HGNC:1", "gene"),
        NodeRecord("UP:P1", "protein"),
    ]
    mapper = NodeIdMapper().build(nodes)
    assert mapper.get_index("gene", "HGNC:1") == 0
    assert mapper.get_index("gene", "HGNC:2") == 1
    assert mapper.get_index("protein", "UP:P1") == 0


def test_mapping_is_independent_of_input_order():
    nodes = [
        NodeRecord("HGNC:2", "gene"),
        NodeRecord("HGNC:1", "gene"),
        NodeRecord("UP:P1", "protein"),
    ]
    forward = NodeIdMapper().build(nodes).as_dict()
    backward = NodeIdMapper().build(reversed(nodes)).as_dict()
    assert forward == backward


def test_same_id_under_different_types_is_rejected():
    nodes = [NodeRecord("A", "gene"), NodeRecord("A", "protein")]
    with pytest.raises(ValueError, match="appears as both 'gene' and 'protein'"):
        NodeIdMapper().build(nodes)


def test_duplicate_id_within_type_is_rejected():
    nodes = [
        NodeRecord("HGNC:1", "gene", {"symbol": "A"}),
        NodeRecord("HGNC:1", "gene", {"symbol": "A-alt"}),
    ]
    with pytest.raises(ValueError, match="Duplicate ID 'HGNC:1'"):
        NodeIdMapper().build(nodes)


def test_identical_duplicate_records_are_rejected():
    node = NodeRecord("HGNC:1", "gene", {"symbol": "A"})
    with pytest.raises(ValueError, match="Duplicate ID 'HGNC:1'"):
        NodeIdMapper().build([node, node])


def test_conversion_rejects_duplicate_node_ids():
    nodes = [NodeRecord("HGNC:1", "gene"), NodeRecord("HGNC:1", "gene")]
    with pytest.raises(ValueError, match="Duplicate ID"):
        BioCypherToPyG.from_records(nodes, []).convert()
