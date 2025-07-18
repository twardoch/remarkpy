#!/usr/bin/env python3
"""
Tests for remarkpy CLI
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from remarkpy.cli import create_parser, format_json, main, read_input, write_output


class TestCLIFunctions:
    """Test CLI utility functions"""

    def test_create_parser(self):
        """Test parser creation"""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "remarkpy"

    def test_read_input_from_file(self):
        """Test reading input from file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nContent")
            temp_path = f.name

        try:
            content = read_input(temp_path)
            assert content == "# Test\n\nContent"
        finally:
            Path(temp_path).unlink()

    def test_write_output_to_file(self):
        """Test writing output to file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            write_output('{"test": "data"}', temp_path)

            with open(temp_path) as f:
                content = f.read()

            assert content == '{"test": "data"}'
        finally:
            Path(temp_path).unlink()

    def test_format_json_pretty(self):
        """Test pretty JSON formatting"""
        data = {"type": "root", "children": [{"type": "heading", "depth": 1}]}
        result = format_json(data, compact=False, indent=2)

        assert '"type": "root"' in result
        assert result.count("\n") > 0  # Should have newlines

    def test_format_json_compact(self):
        """Test compact JSON formatting"""
        data = {"type": "root", "children": [{"type": "heading", "depth": 1}]}
        result = format_json(data, compact=True)

        assert '"type":"root"' in result
        assert "\n" not in result  # Should not have newlines


class TestCLIIntegration:
    """Integration tests for CLI"""

    def test_cli_with_simple_markdown(self):
        """Test CLI with simple markdown file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Hello World\n\nThis is a test.")
            input_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert result.stderr == ""

            # Parse output JSON
            output_data = json.loads(result.stdout)
            assert output_data["type"] == "root"
            assert "children" in output_data
            assert len(output_data["children"]) > 0

        finally:
            Path(input_path).unlink()

    def test_cli_with_output_file(self):
        """Test CLI with output file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Output\n\nSome content.")
            input_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path, "-o", output_path],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert result.stderr == ""

            # Check output file
            with open(output_path) as f:
                content = f.read()

            output_data = json.loads(content)
            assert output_data["type"] == "root"
            assert "children" in output_data

        finally:
            Path(input_path).unlink()
            Path(output_path).unlink()

    def test_cli_with_compact_output(self):
        """Test CLI with compact output"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Compact Test")
            input_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path, "--compact"],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert result.stderr == ""

            # Output should be compact (no extra whitespace)
            output_data = json.loads(result.stdout)
            assert output_data["type"] == "root"

            # Check that output is indeed compact
            assert "\n" not in result.stdout.strip()

        finally:
            Path(input_path).unlink()

    def test_cli_with_verbose_output(self):
        """Test CLI with verbose output"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Verbose Test")
            input_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path, "--verbose"],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert "Initialized RemarkpyParser" in result.stderr
            assert "Parsing" in result.stderr

            # Output should still be valid JSON
            output_data = json.loads(result.stdout)
            assert output_data["type"] == "root"

        finally:
            Path(input_path).unlink()

    def test_cli_with_stdin(self):
        """Test CLI reading from stdin"""
        markdown_content = "# Stdin Test\n\nReading from stdin."

        # Run CLI with stdin
        result = subprocess.run(
            [sys.executable, "-m", "remarkpy.cli", "-"],
            input=markdown_content,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert result.stderr == ""

        # Parse output JSON
        output_data = json.loads(result.stdout)
        assert output_data["type"] == "root"
        assert "children" in output_data

    def test_cli_version(self):
        """Test CLI version output"""
        result = subprocess.run(
            [sys.executable, "-m", "remarkpy.cli", "--version"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "remarkpy" in result.stdout

    def test_cli_help(self):
        """Test CLI help output"""
        result = subprocess.run(
            [sys.executable, "-m", "remarkpy.cli", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout
        assert "Parse Markdown files" in result.stdout

    def test_cli_invalid_file(self):
        """Test CLI with invalid file"""
        result = subprocess.run(
            [sys.executable, "-m", "remarkpy.cli", "/nonexistent/file.md"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "not found" in result.stderr

    def test_cli_with_complex_markdown(self):
        """Test CLI with complex markdown document"""
        complex_markdown = """# Complex Document

This document has various elements.

## Lists

- Item 1
- Item 2
  - Nested item

## Code

```python
def hello():
    print("Hello, World!")
```

## Links

[Link](https://example.com)

## Blockquotes

> This is a quote

## Tables

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(complex_markdown)
            input_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert result.stderr == ""

            # Parse output JSON
            output_data = json.loads(result.stdout)
            assert output_data["type"] == "root"
            assert "children" in output_data
            assert len(output_data["children"]) > 5  # Should have many elements

        finally:
            Path(input_path).unlink()

    def test_cli_with_unicode(self):
        """Test CLI with unicode content"""
        unicode_markdown = """# Unicode Test 🚀

This has various unicode characters:
- émojis: 😀 🎉 🌟
- accented chars: áéíóú
- other scripts: 日本語 العربية
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(unicode_markdown)
            input_path = f.name

        try:
            # Run CLI
            result = subprocess.run(
                [sys.executable, "-m", "remarkpy.cli", input_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            assert result.returncode == 0
            assert result.stderr == ""

            # Parse output JSON
            output_data = json.loads(result.stdout)
            assert output_data["type"] == "root"

        finally:
            Path(input_path).unlink()


class TestCLIErrorHandling:
    """Test CLI error handling"""

    def test_cli_conflicting_options(self):
        """Test CLI with conflicting options"""
        result = subprocess.run(
            [sys.executable, "-m", "remarkpy.cli", "--compact", "--pretty", "-"],
            input="# Test",
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "cannot be used together" in result.stderr

    def test_cli_invalid_json_validation(self):
        """Test CLI JSON validation (should not fail with normal usage)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test")
            input_path = f.name

        try:
            # Run CLI with validation
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "remarkpy.cli",
                    input_path,
                    "--validate",
                    "--verbose",
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert "JSON validation passed" in result.stderr

        finally:
            Path(input_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__])
