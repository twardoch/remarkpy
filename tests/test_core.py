#!/usr/bin/env python3
"""
Tests for remarkpy.core module
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from remarkpy.core import JavaScriptError, RemarkpyError, RemarkpyParser


class TestRemarkpyParser:
    """Test cases for RemarkpyParser class"""

    def setup_method(self):
        """Setup parser for each test"""
        self.parser = RemarkpyParser()

    def test_parser_initialization(self):
        """Test that parser initializes correctly"""
        assert self.parser is not None
        assert hasattr(self.parser, "parse")
        assert hasattr(self.parser, "_parse_md_func")

    def test_simple_markdown_parsing(self):
        """Test parsing simple markdown"""
        markdown = "# Hello World"
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert "children" in result
        assert len(result["children"]) > 0

        # Check for heading
        heading = result["children"][0]
        assert heading["type"] == "heading"
        assert heading["depth"] == 1

    def test_complex_markdown_parsing(self):
        """Test parsing complex markdown with multiple elements"""
        markdown = """# Main Title

This is a paragraph with **bold** and *italic* text.

## Subsection

- List item 1
- List item 2
- List item 3

```python
def hello():
    print("Hello World")
```

> This is a blockquote

[Link text](https://example.com)
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert "children" in result

        # Should have multiple children (heading, paragraph, heading, list, code, blockquote, paragraph)
        assert len(result["children"]) >= 5

        # Check for different node types
        node_types = [child["type"] for child in result["children"]]
        assert "heading" in node_types
        assert "paragraph" in node_types
        assert "list" in node_types
        assert "code" in node_types
        assert "blockquote" in node_types

    def test_empty_string_parsing(self):
        """Test parsing empty string"""
        result = self.parser.parse("")

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert "children" in result
        # Empty string should result in empty children array
        assert len(result["children"]) == 0

    def test_whitespace_only_parsing(self):
        """Test parsing whitespace-only string"""
        result = self.parser.parse("   \n\n  \t  ")

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert "children" in result
        # Whitespace only should result in empty or minimal children
        assert len(result["children"]) == 0

    def test_markdown_with_html(self):
        """Test parsing markdown with HTML elements"""
        markdown = """# Title

<div>HTML content</div>

Regular **markdown** continues.
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert len(result["children"]) >= 2

    def test_markdown_with_tables(self):
        """Test parsing markdown with tables"""
        markdown = """| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        # Note: Table support depends on the md-mdast configuration
        # This test verifies the parser doesn't crash on tables

    def test_invalid_input_type(self):
        """Test error handling for invalid input types"""
        with pytest.raises(TypeError, match="Input markdown_text must be a string"):
            self.parser.parse(123)

        with pytest.raises(TypeError, match="Input markdown_text must be a string"):
            self.parser.parse(None)

        with pytest.raises(TypeError, match="Input markdown_text must be a string"):
            self.parser.parse(["not", "a", "string"])

    def test_unicode_handling(self):
        """Test handling of unicode characters"""
        markdown = """# Unicode Test 🚀

This has émojis and spëcial characters: áéíóú

## 日本語のテスト

- Item with 中文
- Another item with العربية
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert len(result["children"]) >= 2

    def test_very_long_markdown(self):
        """Test parsing very long markdown document"""
        # Create a long markdown document
        sections = []
        for i in range(100):
            sections.append(
                f"## Section {i}\n\nThis is paragraph {i} with some **bold** text.\n"
            )

        markdown = "\n".join(sections)
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert len(result["children"]) >= 100  # Should have many children

    def test_markdown_with_code_blocks(self):
        """Test parsing various code block formats"""
        markdown = """```python
def hello():
    print("Hello")
```

```javascript
function hello() {
    console.log("Hello");
}
```

    # Indented code block
    def indented():
        pass

`inline code`
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"

        # Should contain code blocks
        node_types = [child["type"] for child in result["children"]]
        assert "code" in node_types

    def test_markdown_links_and_images(self):
        """Test parsing links and images"""
        markdown = """[Regular link](https://example.com)

[Link with title](https://example.com "Title")

![Alt text](https://example.com/image.png)

![Image with title](https://example.com/image.png "Image title")

<https://autolink.com>
"""
        result = self.parser.parse(markdown)

        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert len(result["children"]) >= 1


class TestRemarkpyParserErrors:
    """Test error handling in RemarkpyParser"""

    def test_missing_js_file(self, monkeypatch):
        """Test error when JavaScript file is missing"""
        # Mock the file path to a non-existent file
        import remarkpy.core

        monkeypatch.setattr(remarkpy.core, "_JS_FILE_PATH", "/nonexistent/path.js")

        with pytest.raises(
            RemarkpyError, match="JavaScript bundle remarkpy.js not found"
        ):
            RemarkpyParser()

    def test_corrupted_js_file(self, monkeypatch):
        """Test error when JavaScript file is corrupted"""
        # Create a temporary corrupted JS file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write("invalid javascript syntax {{{")
            corrupted_path = f.name

        try:
            import remarkpy.core

            monkeypatch.setattr(remarkpy.core, "_JS_FILE_PATH", corrupted_path)

            with pytest.raises(
                JavaScriptError, match="Error initializing JavaScript parseMd function"
            ):
                RemarkpyParser()
        finally:
            os.unlink(corrupted_path)


class TestUtilityFunctions:
    """Test utility functions and edge cases"""

    def setup_method(self):
        """Setup parser for each test"""
        self.parser = RemarkpyParser()

    def test_test_md_file_parsing(self):
        """Test parsing the test.md file if it exists"""
        test_md_path = Path(__file__).parent.parent / "remarkpy" / "test.md"

        if test_md_path.exists():
            with open(test_md_path, encoding="utf-8") as f:
                markdown = f.read()

            result = self.parser.parse(markdown)

            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert "children" in result

    def test_result_serialization(self):
        """Test that results can be serialized to JSON"""
        markdown = "# Test\n\nParagraph with **bold** text."
        result = self.parser.parse(markdown)

        # Should be able to serialize to JSON
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

        # Should be able to deserialize back
        deserialized = json.loads(json_str)
        assert deserialized == result

    def test_consistent_results(self):
        """Test that parsing the same markdown multiple times gives consistent results"""
        markdown = "# Consistency Test\n\nThis should always parse the same way."

        result1 = self.parser.parse(markdown)
        result2 = self.parser.parse(markdown)
        result3 = self.parser.parse(markdown)

        assert result1 == result2 == result3

    def test_parser_reuse(self):
        """Test that parser can be reused multiple times"""
        parser = RemarkpyParser()

        # Parse different markdown strings
        results = []
        for i in range(10):
            markdown = f"# Test {i}\n\nParagraph {i}"
            result = parser.parse(markdown)
            results.append(result)

        # All results should be valid
        for result in results:
            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert len(result["children"]) >= 1


if __name__ == "__main__":
    pytest.main([__file__])
