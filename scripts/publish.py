#!/usr/bin/env python3
"""
Publishing script for django-metachoices package.
Automates version bumping and PyPI publishing.
"""

import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def get_current_version():
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def bump_version(current_version, bump_type):
    """Bump version based on type (patch, minor, major)."""
    major, minor, patch = map(int, current_version.split("."))

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("bump_type must be 'patch', 'minor', or 'major'")

    return f"{major}.{minor}.{patch}"


def update_version_files(new_version):
    """Update version in pyproject.toml and __init__.py."""
    # Update pyproject.toml - be more specific to avoid matching ruff target-version
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    # Only match the project version, not ruff target-version
    content = re.sub(r'(\[project\][\s\S]*?)version = "[^"]+"', f'\\1version = "{new_version}"', content)
    pyproject_path.write_text(content)

    # Update __init__.py
    init_path = Path("metachoices/__init__.py")
    content = init_path.read_text()
    content = re.sub(
        r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', content
    )
    init_path.write_text(content)

    print(f"Updated version to {new_version}")


def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning build artifacts...")
    cmd = (
        "Remove-Item -Recurse -Force dist/, build/, django_metachoices.egg-info/ "
        "-ErrorAction SilentlyContinue"
    )
    run_command(cmd, check=False)


def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")


def check_package():
    """Validate the package."""
    print("Validating package...")
    run_command("twine check dist/*")


def upload_package(test=False):
    """Upload package to PyPI or TestPyPI."""
    if test:
        print("Uploading to TestPyPI...")
        run_command("twine upload --repository testpypi dist/*")
    else:
        print("Uploading to PyPI...")
        run_command("twine upload dist/*")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python publish.py <patch|minor|major> [--test]")
        print("Example: python publish.py patch")
        print("Example: python publish.py minor --test")
        sys.exit(1)

    bump_type = sys.argv[1]
    test_upload = "--test" in sys.argv

    if bump_type not in ["patch", "minor", "major"]:
        print("Error: bump_type must be 'patch', 'minor', or 'major'")
        sys.exit(1)

    try:
        # Get current version and bump it
        current_version = get_current_version()
        new_version = bump_version(current_version, bump_type)

        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")

        # Confirm with user
        confirm = input("Continue? (y/N): ")
        if confirm.lower() != "y":
            print("Aborted.")
            sys.exit(0)

        # Update version files
        update_version_files(new_version)

        # Sync metadata to ensure consistency
        print("Syncing metadata...")
        run_command("python scripts/sync_metadata.py")

        # Clean, build, check, and upload
        clean_build()
        build_package()
        check_package()
        upload_package(test=test_upload)

        print(f"Successfully published version {new_version}!")

        if test_upload:
            print("Package uploaded to TestPyPI")
            print(
                f"View at: https://test.pypi.org/project/django-metachoices/{new_version}/"
            )
        else:
            print("Package uploaded to PyPI")
            print(
                f"View at: https://pypi.org/project/django-metachoices/{new_version}/"
            )

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
