#!/usr/bin/env python3
"""
Release script for remarkpy
Handles version bumping, tagging, and publishing
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, cwd=None, check=True, capture_output=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    if isinstance(cmd, str):
        cmd = cmd.split()

    result = subprocess.run(cmd, cwd=cwd, capture_output=capture_output, text=True)

    if capture_output:
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


def get_current_version():
    """Get the current version from git tags"""
    try:
        result = run_command("git describe --tags --abbrev=0", capture_output=True)
        tag = result.stdout.strip()
        if tag.startswith("v"):
            return tag[1:]  # Remove 'v' prefix
        return tag
    except subprocess.CalledProcessError:
        return "0.0.0"


def parse_version(version_str):
    """Parse a semantic version string"""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-(.+))?", version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")

    major, minor, patch = map(int, match.groups()[:3])
    prerelease = match.group(4)

    return major, minor, patch, prerelease


def bump_version(current_version, bump_type):
    """Bump version according to semver rules"""
    major, minor, patch, prerelease = parse_version(current_version)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return f"{major}.{minor}.{patch}"


def update_changelog(version, changes=None):
    """Update CHANGELOG.md with new version"""
    project_root = get_project_root()
    changelog_path = project_root / "CHANGELOG.md"

    if not changelog_path.exists():
        # Create new changelog
        with open(changelog_path, "w") as f:
            f.write("# Changelog\n\n")
            f.write(
                "All notable changes to this project will be documented in this file.\n\n"
            )
            f.write(
                "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\n"
            )
            f.write(
                "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
            )

    # Read current changelog
    with open(changelog_path) as f:
        content = f.read()

    # Get current date
    date = datetime.now().strftime("%Y-%m-%d")

    # Prepare new entry
    new_entry = f"## [{version}] - {date}\n\n"

    if changes:
        new_entry += changes + "\n\n"
    else:
        # Generate changelog from git commits since last tag
        try:
            last_tag = run_command(
                "git describe --tags --abbrev=0", capture_output=True
            ).stdout.strip()
            commits = run_command(
                f"git log {last_tag}..HEAD --oneline", capture_output=True
            ).stdout.strip()

            if commits:
                new_entry += "### Changed\n\n"
                for commit in commits.split("\n"):
                    if commit.strip():
                        new_entry += f"- {commit.strip()}\n"
                new_entry += "\n"
        except subprocess.CalledProcessError:
            new_entry += "### Changed\n\n- Initial release\n\n"

    # Insert new entry after the header
    lines = content.split("\n")
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            header_end = i
            break

    if header_end == 0:
        # No existing entries, find end of header
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 5:  # Skip initial header
                header_end = i + 1
                break

    # Insert new entry
    lines.insert(header_end, new_entry.rstrip())

    # Write updated changelog
    with open(changelog_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Updated changelog with version {version}")


def check_working_directory():
    """Check that working directory is clean"""
    result = run_command("git status --porcelain", capture_output=True)
    if result.stdout.strip():
        print("Working directory is not clean:")
        print(result.stdout)
        return False
    return True


def create_git_tag(version):
    """Create and push git tag"""
    tag_name = f"v{version}"

    # Create tag
    run_command(f"git tag -a {tag_name} -m 'Release {version}'")

    # Push tag
    run_command(f"git push origin {tag_name}")

    print(f"Created and pushed tag: {tag_name}")


def publish_to_pypi(test=False):
    """Publish package to PyPI"""
    project_root = get_project_root()

    # Install twine if not available
    try:
        run_command("twine --version", capture_output=True)
    except subprocess.CalledProcessError:
        print("Installing twine...")
        run_command([sys.executable, "-m", "pip", "install", "twine"])

    # Check distribution
    dist_dir = project_root / "dist"
    if not dist_dir.exists() or not list(dist_dir.glob("*.whl")):
        raise FileNotFoundError("No distribution files found. Run build first.")

    # Upload to PyPI
    if test:
        print("Uploading to Test PyPI...")
        run_command(f"twine upload --repository testpypi {dist_dir}/*")
    else:
        print("Uploading to PyPI...")
        run_command(f"twine upload {dist_dir}/*")

    print("Package published successfully!")


def main():
    """Main release function"""
    parser = argparse.ArgumentParser(description="Release script for remarkpy")
    parser.add_argument(
        "bump_type", choices=["major", "minor", "patch"], help="Type of version bump"
    )
    parser.add_argument("--version", help="Specific version to release")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    parser.add_argument("--test-pypi", action="store_true", help="Upload to Test PyPI")
    parser.add_argument("--skip-build", action="store_true", help="Skip building")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-publish", action="store_true", help="Skip publishing")
    parser.add_argument("--changes", help="Changelog entry for this release")

    args = parser.parse_args()

    project_root = get_project_root()

    try:
        # Check working directory
        if not args.dry_run and not check_working_directory():
            print("Please commit or stash changes before releasing")
            sys.exit(1)

        # Determine version
        if args.version:
            new_version = args.version
        else:
            current_version = get_current_version()
            new_version = bump_version(current_version, args.bump_type)

        print(f"Releasing version {new_version}")

        if args.dry_run:
            print("DRY RUN - Would perform the following actions:")
            print(f"1. Update version to {new_version}")
            print("2. Build JavaScript bundle")
            print("3. Run tests")
            print("4. Build Python package")
            print("5. Update changelog")
            print("6. Create git tag")
            print("7. Publish to PyPI")
            return

        # Build the package
        if not args.skip_build:
            print("Building package...")
            build_script = project_root / "scripts" / "build.py"
            cmd = [sys.executable, str(build_script)]

            if args.skip_tests:
                cmd.append("--no-tests")

            if args.version:
                cmd.extend(["--version", new_version])

            run_command(cmd, cwd=project_root)

        # Update changelog
        update_changelog(new_version, args.changes)

        # Commit changelog
        run_command("git add CHANGELOG.md")
        run_command(f"git commit -m 'Update changelog for {new_version}'")

        # Create git tag
        create_git_tag(new_version)

        # Publish to PyPI
        if not args.skip_publish:
            publish_to_pypi(test=args.test_pypi)

        print(f"Release {new_version} completed successfully!")

    except Exception as e:
        print(f"Release failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
