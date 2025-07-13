@echo off
echo Building and testing django-metachoices package

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info

REM Install development dependencies
echo Installing development dependencies...
pip install -e .[dev]
if %errorlevel% neq 0 (
    echo Failed to install development dependencies
    exit /b 1
)

REM Run code formatting
echo Formatting code with black...
black django_metachoices tests
if %errorlevel% neq 0 (
    echo Failed to format code
    exit /b 1
)

echo Sorting imports with isort...
isort django_metachoices tests
if %errorlevel% neq 0 (
    echo Failed to sort imports
    exit /b 1
)

REM Run linting
echo Linting with flake8...
flake8 django_metachoices tests
if %errorlevel% neq 0 (
    echo Failed linting
    exit /b 1
)

REM Run type checking
echo Type checking with mypy...
mypy django_metachoices
if %errorlevel% neq 0 (
    echo Failed type checking
    exit /b 1
)

REM Run tests
echo Running tests...
pytest --cov=django_metachoices --cov-report=term-missing
if %errorlevel% neq 0 (
    echo Failed tests
    exit /b 1
)

REM Build package
echo Building package...
python -m build
if %errorlevel% neq 0 (
    echo Failed to build package
    exit /b 1
)

REM Check package
echo Checking package...
twine check dist/*
if %errorlevel% neq 0 (
    echo Failed package check
    exit /b 1
)

echo.
echo All checks passed! Package is ready for publication.
echo.
echo To publish to PyPI:
echo   1. Test PyPI: twine upload --repository testpypi dist/*
echo   2. Production PyPI: twine upload dist/* 