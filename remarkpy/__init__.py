"""
Remarkpy: Python interface to the UnifiedJS/RemarkJS world for Markdown processing.
"""

from .core import JavaScriptError, RemarkpyError, RemarkpyParser

try:
    from ._version import __version__
except ImportError:
    # Fallback for development installations
    __version__ = "0.1.0-dev"

__all__ = [
    "RemarkpyParser",
    "RemarkpyError",
    "JavaScriptError",
    "__version__",
]
