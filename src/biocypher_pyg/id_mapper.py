"""Deterministic, per-node-type ID/index mapping."""

from __future__ import annotations


class NodeIdMapper:
    def __init__(self) -> None:
        self._id_to_index: dict[str, dict[str, int]] = {}
        self._index_to_id: dict[str, list[str]] = {}

    def build(self, nodes) -> NodeIdMapper:
        """Assign deterministic per-type indices to node identifiers.

        Identifiers must be unique across the whole graph, as in BioCypher,
        where node IDs are graph-wide (typically CURIEs). Within each node
        type, indices follow the lexicographic order of the identifiers.

        Args:
            nodes: Iterable of ``NodeRecord`` objects with normalized types.

        Returns:
            This mapper, populated.

        Raises:
            ValueError: If an identifier occurs more than once, either under
                the same node type or under different node types.
        """
        grouped: dict[str, list[str]] = {}
        seen_types: dict[str, str] = {}
        for node in nodes:
            previous = seen_types.get(node.node_id)
            if previous == node.node_type:
                raise ValueError(
                    f"Duplicate ID {node.node_id!r} for node type {previous!r}"
                )
            if previous is not None:
                raise ValueError(
                    f"ID {node.node_id!r} appears as both {previous!r} "
                    f"and {node.node_type!r}"
                )
            seen_types[node.node_id] = node.node_type
            grouped.setdefault(node.node_type, []).append(node.node_id)

        for node_type, ids in grouped.items():
            ordered = sorted(ids)
            self._index_to_id[node_type] = ordered
            self._id_to_index[node_type] = {
                original_id: index for index, original_id in enumerate(ordered)
            }
        return self

    @property
    def node_types(self) -> list[str]:
        return sorted(self._id_to_index)

    def get_index(self, node_type: str, original_id: str) -> int:
        try:
            return self._id_to_index[node_type][original_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown node ID {original_id!r} for type {node_type!r}"
            ) from exc

    def get_original_id(self, node_type: str, index: int) -> str:
        try:
            return self._index_to_id[node_type][index]
        except (KeyError, IndexError) as exc:
            raise KeyError(
                f"Unknown node index {index!r} for type {node_type!r}"
            ) from exc

    def as_dict(self) -> dict[str, list[str]]:
        return {key: list(value) for key, value in self._index_to_id.items()}

    @classmethod
    def from_dict(cls, mapping: dict[str, list[str]]) -> NodeIdMapper:
        mapper = cls()
        for node_type, ids in mapping.items():
            if len(ids) != len(set(ids)):
                raise ValueError(f"Duplicate IDs in mapping for {node_type!r}")
            mapper._index_to_id[node_type] = list(ids)
            mapper._id_to_index[node_type] = {
                original_id: index for index, original_id in enumerate(ids)
            }
        return mapper
