#!/usr/bin/env python3
"""
Integration tests for remarkpy package
"""

import json
from pathlib import Path

import pytest

import remarkpy
from remarkpy import JavaScriptError, RemarkpyError, RemarkpyParser


class TestPackageIntegration:
    """Integration tests for the complete package"""

    def test_package_imports(self):
        """Test that all expected classes and functions can be imported"""
        # Test direct imports
        from remarkpy import JavaScriptError, RemarkpyError, RemarkpyParser

        # Test that classes are accessible
        assert RemarkpyParser is not None
        assert RemarkpyError is not None
        assert JavaScriptError is not None

        # Test package-level access
        assert hasattr(remarkpy, "RemarkpyParser")
        assert hasattr(remarkpy, "RemarkpyError")
        assert hasattr(remarkpy, "JavaScriptError")
        assert hasattr(remarkpy, "__version__")

    def test_version_availability(self):
        """Test that version information is available"""
        assert remarkpy.__version__ is not None
        assert isinstance(remarkpy.__version__, str)
        assert len(remarkpy.__version__) > 0

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Initialize parser
        parser = RemarkpyParser()

        # Parse a comprehensive markdown document
        markdown = """# Complete Markdown Example

This document tests various markdown features.

## Text Formatting

This paragraph contains **bold text**, *italic text*, and `inline code`.

## Lists

### Unordered List
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3

### Ordered List
1. First item
2. Second item
3. Third item

## Code Blocks

```python
def example_function():
    \"\"\"Example function\"\"\"
    return "Hello, World!"
```

## Links and Images

[Link to example](https://example.com)

![Alt text](https://example.com/image.png)

## Blockquotes

> This is a blockquote
> with multiple lines
> and **formatting**.

## Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Horizontal Rule

---

## HTML in Markdown

<div>
  <p>HTML content within markdown</p>
</div>

## Task Lists

- [x] Completed task
- [ ] Incomplete task
- [ ] Another incomplete task

## Footnotes

This has a footnote[^1].

[^1]: This is the footnote.
"""

        # Parse the markdown
        result = parser.parse(markdown)

        # Verify the result structure
        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert "children" in result
        assert len(result["children"]) > 10  # Should have many elements

        # Verify JSON serialization works
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

        # Verify deserialization works
        deserialized = json.loads(json_str)
        assert deserialized == result

    def test_real_world_markdown_files(self):
        """Test parsing real-world markdown files from the project"""
        project_root = Path(__file__).parent.parent

        # Test README.md
        readme_path = project_root / "README.md"
        if readme_path.exists():
            parser = RemarkpyParser()

            with open(readme_path, encoding="utf-8") as f:
                markdown = f.read()

            result = parser.parse(markdown)

            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert "children" in result
            assert len(result["children"]) > 0

        # Test CHANGELOG.md
        changelog_path = project_root / "CHANGELOG.md"
        if changelog_path.exists():
            parser = RemarkpyParser()

            with open(changelog_path, encoding="utf-8") as f:
                markdown = f.read()

            result = parser.parse(markdown)

            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert "children" in result

        # Test test.md from remarkpy directory
        test_md_path = project_root / "remarkpy" / "test.md"
        if test_md_path.exists():
            parser = RemarkpyParser()

            with open(test_md_path, encoding="utf-8") as f:
                markdown = f.read()

            result = parser.parse(markdown)

            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert "children" in result

    def test_concurrent_parsers(self):
        """Test that multiple parsers can work concurrently"""
        import threading
        import time

        results = []
        errors = []

        def parse_markdown(markdown, parser_id):
            try:
                parser = RemarkpyParser()
                result = parser.parse(
                    f"# Parser {parser_id}\n\nContent from parser {parser_id}"
                )
                results.append((parser_id, result))
            except Exception as e:
                errors.append((parser_id, e))

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=parse_markdown, args=(f"# Test {i}", i))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5

        # Verify all results are valid
        for parser_id, result in results:
            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert len(result["children"]) >= 1

    def test_memory_usage(self):
        """Test that the parser doesn't leak memory with repeated use"""
        parser = RemarkpyParser()

        # Parse many documents
        for i in range(100):
            markdown = f"""# Document {i}

This is document number {i} with various content:

- List item 1
- List item 2
- List item 3

```python
def function_{i}():
    return {i}
```

> Quote from document {i}
"""
            result = parser.parse(markdown)

            # Verify result
            assert isinstance(result, dict)
            assert result["type"] == "root"
            assert len(result["children"]) >= 3

    def test_edge_cases(self):
        """Test various edge cases"""
        parser = RemarkpyParser()

        # Test markdown with unusual characters
        edge_cases = [
            "# Test\n\n" + "a" * 10000,  # Very long line
            "# Test\n\n" + "\n" * 1000,  # Many empty lines
            "# Test\n\n" + "🚀" * 100,  # Many emoji
            "# Test\n\n" + "```\n" + "code" * 1000 + "\n```",  # Very long code block
        ]

        for markdown in edge_cases:
            result = parser.parse(markdown)
            assert isinstance(result, dict)
            assert result["type"] == "root"


@pytest.mark.slow
class TestPerformance:
    """Performance tests for remarkpy"""

    def test_large_document_performance(self):
        """Test performance with large markdown documents"""
        import time

        # Create a large markdown document
        sections = []
        for i in range(1000):
            sections.append(
                f"""## Section {i}

This is section {i} with various content:

- List item 1 for section {i}
- List item 2 for section {i}
- List item 3 for section {i}

```python
def function_{i}():
    return "result from section {i}"
```

> This is a blockquote from section {i}

---
"""
            )

        large_markdown = "\n".join(sections)

        parser = RemarkpyParser()

        # Time the parsing
        start_time = time.time()
        result = parser.parse(large_markdown)
        end_time = time.time()

        # Verify result
        assert isinstance(result, dict)
        assert result["type"] == "root"
        assert len(result["children"]) >= 1000

        # Performance check (should complete in reasonable time)
        duration = end_time - start_time
        assert duration < 30.0, f"Parsing took too long: {duration:.2f} seconds"


if __name__ == "__main__":
    pytest.main([__file__])
