@echo off
REM Publishing script wrapper for django-metachoices
REM Usage: publish.bat <patch|minor|major> [test]

cd /d "%~dp0\.."
python scripts/publish.py %* 