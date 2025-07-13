#!/usr/bin/env python3
"""
Sync metadata between pyproject.toml and other files.
Ensures single source of truth for package information.
"""

import re
import tomllib
from pathlib import Path


def load_pyproject():
    """Load pyproject.toml data."""
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def update_readme_requirements(pyproject_data):
    """Update README.md requirements section based on pyproject.toml."""
    readme_path = Path("README.md")
    content = readme_path.read_text()

    # Extract Python version requirement
    python_req = pyproject_data["project"]["requires-python"]
    python_version = python_req.replace(">=", "").replace("~=", "").replace("^", "")

    # Extract Django version requirement
    django_deps = [
        dep
        for dep in pyproject_data["project"]["dependencies"]
        if dep.startswith("Django")
    ]
    if django_deps:
        django_req = django_deps[0]
        django_version = (
            django_req.replace("Django>=", "")
            .replace("Django~=", "")
            .replace("Django^", "")
        )
    else:
        django_version = "Unknown"

    # Update requirements section
    requirements_pattern = (
        r"## Requirements\s*\n\n- \*\*Python\*\*:.*\n- \*\*Django\*\*:.*\n"
    )
    new_requirements = f"""## Requirements

- **Python**: {python_version}+
- **Django**: {django_version}+

"""

    updated_content = re.sub(requirements_pattern, new_requirements, content)
    readme_path.write_text(updated_content)
    print(
        f"Updated README.md requirements: Python {python_version}+, Django {django_version}+"
    )


def update_init_version(pyproject_data):
    """Update __init__.py version to match pyproject.toml."""
    init_path = Path("metachoices/__init__.py")
    content = init_path.read_text()

    version = pyproject_data["project"]["version"]
    updated_content = re.sub(
        r'__version__ = "[^"]+"', f'__version__ = "{version}"', content
    )

    init_path.write_text(updated_content)
    print(f"Updated __init__.py version: {version}")


def update_bumpversion_config(pyproject_data):
    """Update .bumpversion.cfg current version."""
    bumpversion_path = Path(".bumpversion.cfg")
    if not bumpversion_path.exists():
        return

    content = bumpversion_path.read_text()
    version = pyproject_data["project"]["version"]

    updated_content = re.sub(
        r"current_version = [^\n]+", f"current_version = {version}", content
    )

    bumpversion_path.write_text(updated_content)
    print(f"Updated .bumpversion.cfg current version: {version}")


def validate_consistency():
    """Validate that key information is consistent across files."""
    pyproject_data = load_pyproject()

    # Check version consistency
    version = pyproject_data["project"]["version"]

    # Check __init__.py
    init_path = Path("metachoices/__init__.py")
    init_content = init_path.read_text()
    init_version_match = re.search(r'__version__ = "([^"]+)"', init_content)

    if init_version_match:
        init_version = init_version_match.group(1)
        if init_version != version:
            print(
                f"Version mismatch: pyproject.toml ({version}) vs __init__.py ({init_version})"
            )
            return False

    print("All versions are consistent")
    return True


def main():
    """Main function."""
    print("Syncing metadata from pyproject.toml...")

    try:
        pyproject_data = load_pyproject()

        # Update files based on pyproject.toml
        update_readme_requirements(pyproject_data)
        update_init_version(pyproject_data)
        update_bumpversion_config(pyproject_data)

        # Validate consistency
        if validate_consistency():
            print("All metadata synchronized successfully!")
        else:
            print("Some inconsistencies remain")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
