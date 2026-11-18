"""Source adapters.

The first stable interface is normalized records. A concrete BioCypher reader
must be implemented against a pinned BioCypher version/output backend.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from .models import EdgeRecord, NodeRecord


class RecordsReader:
    def __init__(
        self,
        nodes: Iterable[NodeRecord],
        edges: Iterable[EdgeRecord],
    ) -> None:
        self._nodes = nodes
        self._edges = edges

    def read_nodes(self) -> Iterator[NodeRecord]:
        yield from self._nodes

    def read_edges(self) -> Iterator[EdgeRecord]:
        yield from self._edges


class BioCypherExportReader:
    """Placeholder for a backend-specific BioCypher export adapter.

    Implement only after choosing and testing a supported BioCypher version
    and export format. Normalize source rows into NodeRecord / EdgeRecord.
    """

    def __init__(self, source, *, config=None) -> None:
        self.source = source
        self.config = config or {}

    def read_nodes(self):
        raise NotImplementedError(
            "BioCypherExportReader needs a backend-specific implementation. "
            "Use RecordsReader for the initial normalized-record workflow."
        )

    def read_edges(self):
        raise NotImplementedError(
            "BioCypherExportReader needs a backend-specific implementation."
        )
