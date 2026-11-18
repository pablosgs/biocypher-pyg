# Known limitations of the scaffold

- No production BioCypher backend reader is implemented yet.
- Feature encoding supports only explicitly selected, fully populated numeric
  properties.
- Arbitrary metadata is retained in a Python sidecar and JSON serialization
  uses `default=str`; complex objects need a future typed serialization format.
- Hyper-relations / n-ary statements need an explicit modeling strategy.
- Incremental mapping is not implemented; deterministic sorting is designed
  for batch conversion.
- The converter currently materializes input records in memory.
- No automatic inverse-edge generation or deduplication is performed.
