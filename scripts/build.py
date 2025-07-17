#!/usr/bin/env python3
"""
Build script for remarkpy
Handles both JavaScript bundling and Python packaging
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    if isinstance(cmd, str):
        cmd = cmd.split()

    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

    return result


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent


def build_javascript():
    """Build the JavaScript bundle"""
    print("Building JavaScript bundle...")

    project_root = get_project_root()
    js_dir = project_root / "remarkpyjs"

    if not js_dir.exists():
        raise FileNotFoundError(f"JavaScript directory not found: {js_dir}")

    # Check if node_modules exists, if not run npm install
    if not (js_dir / "node_modules").exists():
        print("Installing Node.js dependencies...")
        run_command("npm install", cwd=js_dir)

    # Build the JavaScript bundle
    print("Building JavaScript bundle with webpack...")
    run_command("npm run build", cwd=js_dir)

    # Verify the bundle was created
    bundle_path = project_root / "remarkpy" / "remarkpy.js"
    if not bundle_path.exists():
        raise FileNotFoundError(f"JavaScript bundle not found: {bundle_path}")

    print(f"JavaScript bundle built successfully: {bundle_path}")
    return bundle_path


def update_version_in_files(version):
    """Update version in various files"""
    project_root = get_project_root()

    # Update package.json
    package_json_path = project_root / "remarkpyjs" / "package.json"
    if package_json_path.exists():
        with open(package_json_path) as f:
            package_data = json.load(f)

        package_data["version"] = version

        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=4)

        print(f"Updated version in {package_json_path}")


def build_python():
    """Build the Python package"""
    print("Building Python package...")

    project_root = get_project_root()

    # Clean previous builds
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # Build the package
    print("Building wheel and source distribution...")
    run_command([sys.executable, "-m", "build"], cwd=project_root)

    # List built files
    if dist_dir.exists():
        print("Built files:")
        for file in dist_dir.iterdir():
            print(f"  - {file.name}")

    return dist_dir


def run_tests():
    """Run the test suite"""
    print("Running test suite...")

    project_root = get_project_root()

    # Install test dependencies
    print("Installing test dependencies...")
    run_command(
        [sys.executable, "-m", "pip", "install", "-e", ".[test]"], cwd=project_root
    )

    # Run tests
    print("Running pytest...")
    result = run_command(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        print("Tests failed!")
        return False

    print("All tests passed!")
    return True


def run_linting():
    """Run linting and formatting"""
    print("Running linting and formatting...")

    project_root = get_project_root()

    # Install dev dependencies
    print("Installing dev dependencies...")
    run_command(
        [sys.executable, "-m", "pip", "install", "-e", ".[dev]"], cwd=project_root
    )

    # Run black
    print("Running black...")
    result = run_command(
        [sys.executable, "-m", "black", "--check", "remarkpy", "tests", "scripts"],
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        print("Code formatting issues found. Running black to fix...")
        run_command(
            [sys.executable, "-m", "black", "remarkpy", "tests", "scripts"],
            cwd=project_root,
        )

    # Run ruff
    print("Running ruff...")
    result = run_command(
        [sys.executable, "-m", "ruff", "check", "remarkpy", "tests", "scripts"],
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        print("Linting issues found. Attempting to fix...")
        run_command(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--fix",
                "remarkpy",
                "tests",
                "scripts",
            ],
            cwd=project_root,
            check=False,
        )

    print("Linting completed!")


def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description="Build script for remarkpy")
    parser.add_argument(
        "--js-only", action="store_true", help="Build only JavaScript bundle"
    )
    parser.add_argument(
        "--py-only", action="store_true", help="Build only Python package"
    )
    parser.add_argument("--no-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--no-lint", action="store_true", help="Skip linting")
    parser.add_argument("--version", help="Set version number")

    args = parser.parse_args()

    try:
        if args.version:
            update_version_in_files(args.version)

        if not args.py_only:
            build_javascript()

        if not args.no_lint:
            run_linting()

        if not args.no_tests:
            if not run_tests():
                sys.exit(1)

        if not args.js_only:
            build_python()

        print("Build completed successfully!")

    except Exception as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
