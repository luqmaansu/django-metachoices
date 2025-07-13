#!/usr/bin/env python3
"""
Task runner for django-metachoices development.
Provides common development tasks in one place.
"""

import subprocess
import sys


def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def task_test():
    """Run tests with coverage."""
    return run_command("pytest --cov=django_metachoices --cov-report=term-missing")


def task_lint():
    """Run linting checks."""
    return run_command("ruff check django_metachoices tests")


def task_format():
    """Format code."""
    return run_command("ruff format django_metachoices tests")


def task_format_check():
    """Check code formatting."""
    return run_command("ruff format --check django_metachoices tests")


def task_sync():
    """Sync metadata between files."""
    return run_command("python scripts/sync_metadata.py")


def task_build():
    """Build the package."""
    return run_command("python -m build")


def task_clean():
    """Clean build artifacts."""
    cmd = (
        "Remove-Item -Recurse -Force dist/, build/, django_metachoices.egg-info/ "
        "-ErrorAction SilentlyContinue"
    )
    return run_command(cmd)


def task_check():
    """Run all checks (lint, format-check, test)."""
    print("🔍 Running all checks...")
    success = True
    
    print("\n1. Linting...")
    success &= task_lint()
    
    print("\n2. Format checking...")
    success &= task_format_check()
    
    print("\n3. Testing...")
    success &= task_test()
    
    if success:
        print("\n✅ All checks passed!")
    else:
        print("\n❌ Some checks failed!")
    
    return success


def show_help():
    """Show available tasks."""
    print("Available tasks:")
    print("  test         - Run tests with coverage")
    print("  lint         - Run linting checks")
    print("  format       - Format code")
    print("  format-check - Check code formatting")
    print("  sync         - Sync metadata between files")
    print("  build        - Build the package")
    print("  clean        - Clean build artifacts")
    print("  check        - Run all checks (lint, format-check, test)")
    print("  help         - Show this help message")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    task = sys.argv[1]
    
    tasks = {
        "test": task_test,
        "lint": task_lint,
        "format": task_format,
        "format-check": task_format_check,
        "sync": task_sync,
        "build": task_build,
        "clean": task_clean,
        "check": task_check,
        "help": show_help,
    }
    
    if task not in tasks:
        print(f"Unknown task: {task}")
        show_help()
        sys.exit(1)
    
    if task == "help":
        tasks[task]()
    else:
        success = tasks[task]()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 