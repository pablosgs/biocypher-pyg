# BioCypher integration plan

## Important boundary

BioCypher has multiple output and adapter patterns. Do not assume that a graph
written to one backend can be read back through a universal BioCypher API.

## Implementation sequence

1. Pin the BioCypher version in a dedicated integration environment.
2. Select one concrete BioCypher output/backend and a minimal test graph.
3. Verify how nodes, edges, labels/types, properties and provenance are
   represented in that output.
4. Implement a reader that yields `NodeRecord` and `EdgeRecord`.
5. Add fixture-based integration tests using a small, redistributable graph.
6. Document backend/version limitations.

The initial `BioCypherExportReader` is intentionally a placeholder. The
normalized `RecordsReader` allows the rest of the converter to be developed
and tested independently while this audit is underway.
