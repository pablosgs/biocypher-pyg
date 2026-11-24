"""Public conversion API."""

from __future__ import annotations

from dataclasses import dataclass, field

from .converters.edges import group_edges
from .converters.nodes import group_nodes
from .heterodata_builder import build_heterodata
from .id_mapper import NodeIdMapper
from .models import EdgeRecord, GraphMetadata, NodeRecord
from .reader import RecordsReader
from .schema_mapper import SchemaMapper
from .validator import validate_heterodata


@dataclass
class ConversionResult:
    data: object
    metadata: GraphMetadata
    id_mapper: NodeIdMapper
    validation_errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.validation_errors


class BioCypherToPyG:
    def __init__(
        self,
        reader,
        *,
        schema_mapper: SchemaMapper | None = None,
        feature_config: dict[str, list[str]] | None = None,
    ) -> None:
        self.reader = reader
        self.schema_mapper = schema_mapper or SchemaMapper()
        self.feature_config = feature_config or {}

    @classmethod
    def from_records(
        cls,
        nodes,
        edges,
        *,
        schema_mapper: SchemaMapper | None = None,
        feature_config: dict[str, list[str]] | None = None,
    ) -> BioCypherToPyG:
        return cls(
            RecordsReader(nodes, edges),
            schema_mapper=schema_mapper,
            feature_config=feature_config,
        )

    def convert(self) -> ConversionResult:
        nodes = list(self.reader.read_nodes())
        edges = list(self.reader.read_edges())

        # Normalize BioCypher/source labels before creating the ID mapping.
        normalized_nodes = [
            NodeRecord(
                node_id=n.node_id,
                node_type=self.schema_mapper.map_node_type(n.node_type),
                properties=dict(n.properties),
            )
            for n in nodes
        ]
        normalized_edges = [
            EdgeRecord(
                source_id=e.source_id,
                target_id=e.target_id,
                source_type=self.schema_mapper.map_node_type(e.source_type),
                target_type=self.schema_mapper.map_node_type(e.target_type),
                relation_type=self.schema_mapper.map_relation_type(e.relation_type),
                properties=dict(e.properties),
                edge_id=e.edge_id,
            )
            for e in edges
        ]

        mapper = NodeIdMapper().build(normalized_nodes)
        grouped_nodes = group_nodes(normalized_nodes, SchemaMapper())
        grouped_edges = group_edges(normalized_edges, SchemaMapper(), mapper)

        metadata = GraphMetadata(
            node_ids={
                node_type: [node.node_id for node in records]
                for node_type, records in grouped_nodes.items()
            },
            node_properties={
                node_type: [dict(node.properties) for node in records]
                for node_type, records in grouped_nodes.items()
            },
            edge_records={
                edge_type: list(values["properties"])
                for edge_type, values in grouped_edges.items()
            },
            schema_mapping={
                **self.schema_mapper.node_types,
                **self.schema_mapper.relation_types,
            },
            conversion_config={"feature_config": self.feature_config},
        )

        data = build_heterodata(grouped_nodes, grouped_edges, self.feature_config)
        errors = validate_heterodata(data, metadata)

        return ConversionResult(
            data=data,
            metadata=metadata,
            id_mapper=mapper,
            validation_errors=errors,
        )
