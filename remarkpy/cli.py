#!/usr/bin/env python3
"""
Command-line interface for remarkpy
"""

import argparse
import json
import sys
from typing import Optional

from . import __version__
from .core import JavaScriptError, RemarkpyError, RemarkpyParser


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser"""
    parser = argparse.ArgumentParser(
        prog="remarkpy",
        description="Parse Markdown files to Abstract Syntax Tree (AST) using md-mdast",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  remarkpy input.md                    # Parse input.md and output AST to stdout
  remarkpy input.md -o output.json     # Parse input.md and save AST to output.json
  remarkpy input.md --pretty           # Parse input.md and output pretty-printed AST
  remarkpy input.md --compact          # Parse input.md and output compact AST
  echo "# Hello" | remarkpy -          # Parse from stdin
  remarkpy --version                   # Show version information
        """,
    )

    parser.add_argument("input", help='Input Markdown file (use "-" for stdin)')

    parser.add_argument("-o", "--output", help="Output file (default: stdout)")

    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output (default)"
    )

    parser.add_argument("--compact", action="store_true", help="Compact JSON output")

    parser.add_argument(
        "--indent", type=int, default=2, help="JSON indentation level (default: 2)"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parser.add_argument(
        "--validate", action="store_true", help="Validate that the output is valid JSON"
    )

    return parser


def read_input(input_path: str) -> str:
    """Read input from file or stdin"""
    if input_path == "-":
        if sys.stdin.isatty():
            print("Reading from stdin (press Ctrl+D to finish):", file=sys.stderr)
        return sys.stdin.read()

    try:
        with open(input_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{input_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)


def write_output(
    output_data: str, output_path: Optional[str], verbose: bool = False
) -> None:
    """Write output to file or stdout"""
    if output_path is None:
        print(output_data)
        return

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_data)

        if verbose:
            print(f"Output written to '{output_path}'", file=sys.stderr)

    except PermissionError:
        print(f"Error: Permission denied writing to '{output_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error writing to '{output_path}': {e}", file=sys.stderr)
        sys.exit(1)


def format_json(data: dict, compact: bool = False, indent: int = 2) -> str:
    """Format JSON output"""
    if compact:
        return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    else:
        return json.dumps(data, indent=indent, ensure_ascii=False)


def main() -> None:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle conflicting options
    if args.compact and args.pretty:
        print("Error: --compact and --pretty cannot be used together", file=sys.stderr)
        sys.exit(1)

    # Read input
    try:
        markdown_content = read_input(args.input)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)

    # Initialize parser
    try:
        markdown_parser = RemarkpyParser()
        if args.verbose:
            print(
                f"Initialized RemarkpyParser (remarkpy {__version__})", file=sys.stderr
            )

    except RemarkpyError as e:
        print(f"Error initializing parser: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error initializing parser: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse markdown
    try:
        if args.verbose:
            print(
                f"Parsing {len(markdown_content)} characters of markdown...",
                file=sys.stderr,
            )

        ast = markdown_parser.parse(markdown_content)

        if args.verbose:
            print("Parsing completed successfully", file=sys.stderr)

    except JavaScriptError as e:
        print(f"JavaScript error during parsing: {e}", file=sys.stderr)
        sys.exit(1)
    except RemarkpyError as e:
        print(f"Error during parsing: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during parsing: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    try:
        output_data = format_json(ast, compact=args.compact, indent=args.indent)

        # Validate JSON if requested
        if args.validate:
            try:
                json.loads(output_data)
                if args.verbose:
                    print("JSON validation passed", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"JSON validation failed: {e}", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"Error formatting output: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    try:
        write_output(output_data, args.output, args.verbose)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
