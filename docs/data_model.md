# Data model

- `NodeRecord`: source identifier, source node type, arbitrary properties.
- `EdgeRecord`: source/target identifiers and types, relation type, arbitrary
  properties, optional edge identifier.
- `GraphMetadata`: per-type ordered node IDs, node properties, edge metadata,
  schema mapping and conversion configuration.

Node identifiers must be unique across the whole input graph, following
BioCypher, where node IDs (typically CURIEs such as `hgnc:5`) are graph-wide.
`NodeIdMapper` raises `ValueError` when:

- the same identifier appears under two different node types, or
- the same identifier appears more than once under one node type, even when
  the duplicated records are identical.

Duplicates are rejected rather than merged, because merging would silently
choose between, or discard, their properties. Uniqueness is checked after
schema mapping, so two source labels mapped to one PyG type count as the
same type.

PyG integer indices are assigned separately per node type, in lexicographic
order of the original identifiers, so they do not depend on input order.
