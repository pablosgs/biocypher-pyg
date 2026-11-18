from biocypher_pyg.id_mapper import NodeIdMapper
from biocypher_pyg.models import NodeRecord


def test_mapping_is_deterministic_and_type_scoped():
    nodes = [
        NodeRecord("B", "gene"),
        NodeRecord("A", "gene"),
        NodeRecord("A", "protein"),
    ]
    mapper = NodeIdMapper().build(nodes)
    assert mapper.get_index("gene", "A") == 0
    assert mapper.get_index("gene", "B") == 1
    assert mapper.get_index("protein", "A") == 0
