#!/usr/bin/env python
"""Helper script for building and testing the django-metachoices package."""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    else:
        print(f"✅ Success: {description}")
        return True

def main():
    """Main function to build and test the package."""
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Building and testing django-metachoices package")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Clean previous builds
    if not run_command("rm -rf build/ dist/ *.egg-info/", "Cleaning previous builds"):
        return 1
    
    # Install development dependencies
    if not run_command("pip install -e .[dev]", "Installing development dependencies"):
        return 1
    
    # Run code formatting
    if not run_command("black django_metachoices tests", "Formatting code with black"):
        return 1
    
    if not run_command("isort django_metachoices tests", "Sorting imports with isort"):
        return 1
    
    # Run linting
    if not run_command("flake8 django_metachoices tests", "Linting with flake8"):
        return 1
    
    # Run type checking
    if not run_command("mypy django_metachoices", "Type checking with mypy"):
        return 1
    
    # Run tests
    if not run_command("pytest --cov=django_metachoices --cov-report=term-missing", "Running tests"):
        return 1
    
    # Build package
    if not run_command("python -m build", "Building package"):
        return 1
    
    # Check package
    if not run_command("twine check dist/*", "Checking package"):
        return 1
    
    print("\n🎉 All checks passed! Package is ready for publication.")
    print("\nTo publish to PyPI:")
    print("  1. Test PyPI: twine upload --repository testpypi dist/*")
    print("  2. Production PyPI: twine upload dist/*")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 