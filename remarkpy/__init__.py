# -*- coding: utf-8 -*-
"""
Remarkpy: Python interface to the UnifiedJS/RemarkJS world for Markdown processing.
"""

from .core import RemarkpyParser, RemarkpyError, JavaScriptError

__version__ = '0.1.0' # Matches core.py version, will be source of truth later

__all__ = [
    'RemarkpyParser',
    'RemarkpyError',
    'JavaScriptError',
    '__version__',
]
