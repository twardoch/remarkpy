# Remarkpy

**Remarkpy is a Python library that provides an interface to JavaScript Markdown processing, allowing you to parse Markdown text into an Abstract Syntax Tree (AST).**

It leverages the power of existing JavaScript Markdown libraries (`md-mdast`) by running JavaScript code within your Python environment using the `quickjs` engine. This allows Python developers to easily tap into the rich ecosystem of JavaScript-based Markdown tooling.

## Part 1: General Audience

### What does Remarkpy do?

Remarkpy takes a string of Markdown text as input and returns a detailed, structured representation of that Markdown, known as an Abstract Syntax Tree (AST). This AST can then be used for various purposes, such as:

*   Analyzing Markdown content.
*   Transforming Markdown into other formats (though direct HTML conversion is not yet implemented in this version).
*   Building tools that work with Markdown structure.

Currently, Remarkpy focuses on the parsing aspect, utilizing the `md-mdast` JavaScript library to generate the AST.

### Who is it for?

*   **Python Developers:** If you're working on a Python project and need to understand the structure of Markdown documents, Remarkpy provides a straightforward way to do so.
*   **Tool Builders:** Anyone building tools that need to programmatically interact with Markdown content at a structural level.
*   **Content Analysts:** Researchers or developers who need to analyze patterns or extract information from Markdown files.

### Why is it useful?

*   **Leverage JavaScript Ecosystem:** Access robust and well-maintained JavaScript Markdown libraries from within Python.
*   **Detailed Structural Information:** Get more than just HTML; obtain a full AST for fine-grained control and analysis.
*   **Cross-Language Consistency:** Potentially use the same Markdown parsing logic as a JavaScript-based frontend or other tools.

### Installation

Remarkpy is not yet available on PyPI. To install it, you would typically clone the repository and integrate it into your project, or install it locally using pip once a `setup.py` or `pyproject.toml` is provided.

For now, ensure you have Python 3 and the `quickjs` library installed:

```bash
pip install quickjs
```

You will also need the `remarkpy.js` file (the bundled JavaScript code) to be accessible by the `remarkpy/core.py` module, which it is by default if you are running from the cloned repository.

### How to Use

#### Programmatic Usage (Python)

The primary way to use Remarkpy is through its `RemarkpyParser` class.

```python
from remarkpy.core import RemarkpyParser, RemarkpyError, JavaScriptError
import json

# Initialize the parser
try:
    parser = RemarkpyParser()
except RemarkpyError as e:
    print(f"Failed to initialize parser: {e}")
    exit()

# Markdown text to parse
markdown_input = """
# My Document

This is a paragraph with **bold** and *italic* text.

- Item 1
- Item 2
"""

try:
    # Parse the Markdown
    ast = parser.parse(markdown_input)

    # Print the resulting AST (as a JSON string for readability)
    print("Markdown AST:")
    print(json.dumps(ast, indent=2))

except JavaScriptError as e:
    print(f"An error occurred in the JavaScript code: {e}")
except RemarkpyError as e:
    print(f"A Remarkpy error occurred: {e}")
except TypeError as e:
    print(f"Type error: {e}")

```

#### Command-Line Interface (CLI)

Remarkpy does not have a dedicated CLI tool in this version. However, the `remarkpy/core.py` script can be run directly to parse a predefined Markdown string or a `test.md` file if available in the expected location, which demonstrates its basic functionality:

```bash
python remarkpy/core.py
```
This will print the AST of the example Markdown snippets found within `core.py`.

## Part 2: Technical Details

### How the Code Works

Remarkpy acts as a bridge between Python and JavaScript for Markdown parsing:

1.  **Python Core (`remarkpy/core.py`):**
    *   The `RemarkpyParser` class is the main entry point.
    *   Upon initialization, it reads the bundled JavaScript file (`remarkpy/remarkpy.js`).
    *   It uses the `quickjs` library to create a JavaScript runtime environment and load the `parseMd` function from `remarkpy.js`.
    *   The `parse(markdown_text)` method takes a Markdown string, passes it to the JavaScript `parseMd` function, and receives the resulting AST (as a Python dictionary).
    *   It includes custom error classes (`RemarkpyError`, `JavaScriptError`) for better error handling.

2.  **JavaScript Bridge (`remarkpy/remarkpy.js`):**
    *   This is a browserified JavaScript bundle generated by Webpack (see `remarkpyjs/webpack.config.js`). It contains all necessary JavaScript code to run independently.
    *   The primary source for this bundle is `remarkpyjs/index.js`.

3.  **JavaScript Logic (`remarkpyjs/index.js`):**
    *   This file defines the `parseMd(md)` function.
    *   It uses the `md-mdast` library (a Markdown parser that generates an AST conforming to the Unist specification).
    *   `md-mdast`'s `create().tokenizeBlock(md)` method is called to perform the actual parsing of the Markdown string into an AST.

4.  **QuickJS Integration:**
    *   The `quickjs` Python library allows embedding the QuickJS JavaScript engine.
    *   It enables calling JavaScript functions from Python and transparently converts data types between the two languages (e.g., JavaScript objects to Python dictionaries).

### Coding and Contribution Rules

*   **Licensing:** The project is licensed under the terms specified in the `LICENSE` file. Please review it before contributing.
*   **Coding Style:**
    *   **Python:** Follow PEP 8 guidelines for Python code. Use a linter like Flake8 to check your code.
    *   **JavaScript:** Follow standard JavaScript best practices. Consider using a linter like ESLint if not already configured.
*   **Testing:**
    *   Basic tests and examples are included in `remarkpy/core.py` (within the `if __name__ == '__main__':` block) and `remarkpy/test.py`.
    *   `remarkpy/test.md` provides a sample Markdown file for testing.
    *   The JavaScript part (`md-mdast`) has its own comprehensive tests.
    *   Before submitting contributions, ensure your changes work correctly and do not break existing functionality. Consider adding new test cases for new features.
*   **JavaScript Bundling:**
    *   The JavaScript code in `remarkpyjs/` is bundled into `remarkpy/remarkpy.js` using Webpack. The configuration for this is in `remarkpyjs/webpack.config.js`.
    *   If you make changes to the JavaScript source files in `remarkpyjs/`, you will need to rebuild the bundle. Typically, this involves running a command like `npm run build` or `npx webpack` from within the `remarkpyjs/` directory (assuming Node.js and npm/npx are installed and a `package.json` script is set up). The current `package.json` (in `remarkpyjs/`) defines `build` and `build-dev` scripts.
        ```bash
        cd remarkpyjs
        npm install # if you haven't already
        npm run build # or npm run build-dev for development
        cd ..
        ```
*   **Commit Messages:** Write clear and descriptive commit messages.
*   **Changelog:** For significant changes, update `CHANGELOG.md`.
*   **TODOs:** Check `TODO.md` for planned features or improvements if you are looking for ways to contribute.
*   **Pull Requests:** Submit changes via pull requests. Ensure your code is well-tested and adheres to the project's coding style.

---

This README aims to provide a comprehensive overview. For further details, please refer to the source code and the documentation of the libraries used (QuickJS, md-mdast).
