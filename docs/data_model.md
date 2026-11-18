# Data model

- `NodeRecord`: source identifier, source node type, arbitrary properties.
- `EdgeRecord`: source/target identifiers and types, relation type, arbitrary
  properties, optional edge identifier.
- `GraphMetadata`: per-type ordered node IDs, node properties, edge metadata,
  schema mapping and conversion configuration.

IDs are scoped by node type for PyG indexing. The same lexical identifier may
therefore occur in different node-type namespaces, but an input identifier
appearing under conflicting types is rejected by the initial mapper.
