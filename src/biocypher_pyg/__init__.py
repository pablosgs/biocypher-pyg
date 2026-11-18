"""BioCypher to PyTorch Geometric conversion utilities."""

from .converter import BioCypherToPyG, ConversionResult
from .models import EdgeRecord, GraphMetadata, NodeRecord

__all__ = [
    "BioCypherToPyG",
    "ConversionResult",
    "EdgeRecord",
    "GraphMetadata",
    "NodeRecord",
]

__version__ = "0.1.0.dev0"
