#!/usr/bin/env python3
"""
Binary build script for remarkpy
Creates standalone executables using PyInstaller
"""

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
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


def get_platform_info():
    """Get platform information for binary naming"""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Normalize platform names
    if system == "darwin":
        system = "macos"

    # Normalize architecture names
    if machine in ["x86_64", "amd64"]:
        machine = "x86_64"
    elif machine in ["arm64", "aarch64"]:
        machine = "arm64"
    elif machine in ["i386", "i686"]:
        machine = "x86"

    return system, machine


def create_cli_entry_point():
    """Create a CLI entry point script"""
    project_root = get_project_root()

    # Create temporary CLI script
    cli_script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Entry point for remarkpy CLI binary
\"\"\"

import sys
import os

# Add the current directory to the path to find remarkpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from remarkpy.cli import main

if __name__ == '__main__':
    main()
"""

    cli_path = project_root / "remarkpy_cli.py"
    with open(cli_path, "w") as f:
        f.write(cli_script)

    return cli_path


def create_pyinstaller_spec(cli_path, binary_name, project_root):
    """Create a PyInstaller spec file"""
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{cli_path}'],
    pathex=['{project_root}'],
    binaries=[],
    datas=[
        ('{project_root}/remarkpy/remarkpy.js', 'remarkpy'),
        ('{project_root}/remarkpy/test.md', 'remarkpy'),
    ],
    hiddenimports=[
        'remarkpy',
        'remarkpy.core',
        'remarkpy.cli',
        'quickjs',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{binary_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    spec_path = project_root / f"{binary_name}.spec"
    with open(spec_path, "w") as f:
        f.write(spec_content)

    return spec_path


def build_binary():
    """Build binary with PyInstaller"""
    project_root = get_project_root()
    system, machine = get_platform_info()

    # Determine binary name
    binary_name = f"remarkpy-{system}-{machine}"
    if system == "windows":
        binary_name += ".exe"

    print(f"Building binary: {binary_name}")

    # Install PyInstaller if not available
    try:
        run_command("pyinstaller --version", check=False)
    except FileNotFoundError:
        print("Installing PyInstaller...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Create CLI entry point
    cli_path = create_cli_entry_point()

    try:
        # Create spec file
        spec_path = create_pyinstaller_spec(cli_path, binary_name, project_root)

        # Build with PyInstaller
        run_command(
            f"pyinstaller {spec_path} --distpath dist --workpath build",
            cwd=project_root,
        )

        # Test the binary
        binary_path = project_root / "dist" / binary_name
        if binary_path.exists():
            print(f"Binary built successfully: {binary_path}")

            # Test the binary
            test_markdown = "# Test\n\nThis is a test."
            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
                f.write(test_markdown)
                test_file = f.name

            try:
                print("Testing binary...")
                result = run_command(f"{binary_path} {test_file}", check=False)
                if result.returncode == 0:
                    print("Binary test passed!")
                else:
                    print("Binary test failed!")
                    return False
            finally:
                Path(test_file).unlink()
        else:
            print("Binary not found after build!")
            return False

    finally:
        # Clean up temporary files
        if cli_path.exists():
            cli_path.unlink()

        spec_path = project_root / f"{binary_name}.spec"
        if spec_path.exists():
            spec_path.unlink()

    return True


def build_all_platforms():
    """Build binaries for all platforms (if cross-compilation is supported)"""
    print("Note: Cross-compilation is not supported by PyInstaller.")
    print("Building for current platform only.")
    return build_binary()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Build remarkpy binary")
    parser.add_argument("--all", action="store_true", help="Build for all platforms")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")

    args = parser.parse_args()

    project_root = get_project_root()

    if args.clean:
        print("Cleaning build artifacts...")
        build_dir = project_root / "build"
        if build_dir.exists():
            shutil.rmtree(build_dir)

        # Remove PyInstaller spec files
        for spec_file in project_root.glob("*.spec"):
            spec_file.unlink()

        print("Clean completed.")
        return

    try:
        if args.all:
            success = build_all_platforms()
        else:
            success = build_binary()

        if success:
            print("Binary build completed successfully!")
        else:
            print("Binary build failed!")
            sys.exit(1)

    except Exception as e:
        print(f"Binary build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
