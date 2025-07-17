#!/usr/bin/env python3
"""
Core module for Remarkpy, providing Python bindings to RemarkJS functionality.
"""

__version__ = "0.1.0"  # Initial MVP version

import json
import os
from typing import Any, Dict

import quickjs

# Determine the correct path to remarkpy.js, assuming it's in the same directory as core.py
# This will be important when the package is installed.
_JS_FILE_PATH = os.path.join(os.path.dirname(__file__), "remarkpy.js")


class RemarkpyError(Exception):
    """Base exception for errors raised by Remarkpy."""

    pass


class JavaScriptError(RemarkpyError):
    """Raised when the underlying JavaScript code throws an error."""

    pass


class RemarkpyParser:
    """
    A parser that uses a JavaScript Markdown library (md-mdast) via QuickJS
    to convert Markdown text into an Abstract Syntax Tree (AST).
    """

    def __init__(self):
        """
        Initializes the RemarkpyParser.

        Loads the bundled JavaScript code containing the md-mdast library
        and prepares the JavaScript parsing function.

        Raises:
            RemarkpyError: If the JavaScript file cannot be found or loaded.
            JavaScriptError: If there's an error initializing the JavaScript context.
        """
        try:
            with open(_JS_FILE_PATH, encoding="utf-8") as f:
                js_code = f.read()
        except FileNotFoundError:
            raise RemarkpyError(
                f"Critical: JavaScript bundle remarkpy.js not found at {_JS_FILE_PATH}. "
                "The package might be improperly installed."
            )
        except Exception as e:
            raise RemarkpyError(f"Failed to load JavaScript file: {e}")

        try:
            self._parse_md_func = quickjs.Function("parseMd", js_code)
        except quickjs.JSException as e:
            raise JavaScriptError(
                f"Error initializing JavaScript parseMd function: {e}"
            )
        except Exception as e:  # Catch other potential errors from quickjs
            raise RemarkpyError(f"Unexpected error setting up QuickJS function: {e}")

    def parse(self, markdown_text: str) -> Dict[str, Any]:
        """
        Parses a Markdown string and returns its AST representation.

        Args:
            markdown_text: The Markdown string to parse.

        Returns:
            A dictionary representing the Markdown Abstract Syntax Tree (MDAST).

        Raises:
            TypeError: If markdown_text is not a string.
            JavaScriptError: If the JavaScript `parseMd` function fails.
            RemarkpyError: For other parsing related errors.
        """
        if not isinstance(markdown_text, str):
            raise TypeError("Input markdown_text must be a string.")

        try:
            # The result from quickjs Function call is often already a Python dict/list
            ast = self._parse_md_func(markdown_text)
            if not isinstance(ast, dict):
                # This case should ideally not happen if md-mdast returns a standard AST object
                # but good to have a check.
                raise RemarkpyError(
                    f"JavaScript parser returned an unexpected type: {type(ast)}"
                )
            return ast
        except quickjs.JSException as e:
            raise JavaScriptError(f"JavaScript error during parsing: {e}")
        except Exception as e:
            # Catching broader exceptions that might occur during the call
            raise RemarkpyError(f"An unexpected error occurred during parsing: {e}")


# Example Usage (for testing purposes, can be removed or moved to an example script later)
if __name__ == "__main__":
    parser = RemarkpyParser()

    # Test 1: Simple Markdown
    md_simple = "# Hello World\n\nThis is **bold** and *italic*."
    print(f"Parsing simple Markdown:\n{md_simple}")
    try:
        ast_simple = parser.parse(md_simple)
        print("AST:")
        print(json.dumps(ast_simple, indent=2))
    except RemarkpyError as e:
        print(f"Error: {e}")
    print("-" * 20)

    # Test 2: Using test.md content
    # Assuming test.md is in the parent directory of this script's location (e.g. project root/remarkpy/core.py and project_root/test.md)
    # For robust example, it should be packaged or path handled more carefully
    try:
        # Adjust path to where test.md is expected relative to this file for __main__
        test_md_path = os.path.join(os.path.dirname(__file__), "..", "test.md")
        if os.path.exists(test_md_path):
            with open(test_md_path, encoding="utf-8") as mdf:
                md_from_file = mdf.read()
            print(f"Parsing content from {test_md_path}:")
            ast_from_file = parser.parse(md_from_file)
            print("AST from file:")
            print(json.dumps(ast_from_file, indent=2))
        else:
            print(f"Skipping test.md example, file not found at: {test_md_path}")
    except RemarkpyError as e:
        print(f"Error parsing test.md: {e}")
    except FileNotFoundError:
        print(f"Skipping test.md example, file not found at: {test_md_path}")
    print("-" * 20)

    # Test 3: Empty string
    md_empty = ""
    print(f"Parsing empty string:\n'{md_empty}'")
    try:
        ast_empty = parser.parse(md_empty)
        print("AST (empty string):")
        print(json.dumps(ast_empty, indent=2))
    except RemarkpyError as e:
        print(f"Error: {e}")
    print("-" * 20)

    # Test 4: Invalid input type
    print("Testing invalid input type (integer):")
    try:
        parser.parse(123)
    except TypeError as e:
        print(f"Caught expected error: {e}")
    except RemarkpyError as e:
        print(f"Caught unexpected error: {e}")
    print("-" * 20)

    # Test 5: Simulating JS error by trying to parse a non-string (if JS side doesn't handle it)
    # This depends on how robust the JS `parseMd` is.
    # For now, our Python side `isinstance` check catches this.
    # If we wanted to test JS errors, we might need a special JS function that intentionally errors.
    # print("Simulating JS error (if possible through input):")
    # try:
    #     # This might not actually cause a JS error if parseMd handles non-strings gracefully or if quickjs converts types.
    #     # quickjs might convert None to 'null' or similar.
    #     parser.parse(None)
    # except JavaScriptError as e:
    #     print(f"Caught JavaScript error: {e}")
    # except RemarkpyError as e:
    #     print(f"Caught Remarkpy error: {e}")
