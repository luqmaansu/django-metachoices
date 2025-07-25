# Django Meta Choices

[![PyPI version](https://badge.fury.io/py/django-metachoices.svg)](https://badge.fury.io/py/django-metachoices)
[![Python versions](https://img.shields.io/pypi/pyversions/django-metachoices.svg)](https://pypi.org/project/django-metachoices/)
[![Django versions](https://img.shields.io/pypi/djversions/django-metachoices.svg)](https://pypi.org/project/django-metachoices/)
[![CI](https://github.com/luqmaansu/django-metachoices/workflows/CI/badge.svg)](https://github.com/luqmaansu/django-metachoices/actions)
[![codecov](https://codecov.io/gh/luqmaansu/django-metachoices/branch/main/graph/badge.svg)](https://codecov.io/gh/luqmaansu/django-metachoices)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django field extension that allows choices to have rich metadata beyond the standard (value, display) tuple.

## Overview

Django's standard choice fields only support a simple key-value mapping. This package extends that functionality to allow arbitrary metadata for each choice, which can be accessed through dynamically generated getter methods.

## Example

### Without metachoices

```python

STATUS_CHOICES = {
    "ACTIVE": "Active",
    "INACTIVE": "Inactive",
}

class User(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES) # The normal CharField with choices


# Usage
user = User.objects.create(name="John", status="ACTIVE")

# Access choice data as usual
print(user.status)                    # The database stored value, "ACTIVE"
print(user.get_status_display())      # The human-readable display value, "Active"

```


### With metachoices

```python
from django.db import models
from metachoices import MetaChoiceField

# Define choices with rich metadata
STATUS_CHOICES = {
    "ACTIVE": {
        "display": "Active",
        "color": "#28a745",
        "description": "User is active and can access the system",
        "icon": "check-circle",
        "priority": 1,
    },
    "INACTIVE": {
        "display": "Inactive", 
        "color": "#6c757d",
        "description": "User is inactive and cannot access the system",
        "icon": "x-circle",
        "priority": 2,
    },
}

class User(models.Model):
    name = models.CharField(max_length=100)
    status = MetaChoiceField(choices=STATUS_CHOICES) # Use MetaChoiceField with choices instead of CharField

# Usage
user = User.objects.create(name="John", status="ACTIVE")

# Access choice data as usual
print(user.status)                    # The database stored value, "ACTIVE"
print(user.get_status_display())      # The human-readable display value, "Active"

# With richer capabilities!
print(user.get_status_color())        # "#28a745"
print(user.get_status_description())  # "User is active and can access the system"
print(user.get_status_icon())         # "check-circle"
print(user.get_status_priority())     # 1
```

## Features

- **Rich Metadata**: Add any number of attributes to your choices (description, url, icon, priority, etc.)
- **Dynamic Getters**: Automatically generates `get_<field>_<attribute>()` methods for all metadata attributes
- **Django Compatible**: Works seamlessly with Django's existing choice field functionality
- **Admin Integration**: Fully compatible with Django admin
- **Type Safe**: Validates that field values are valid choice keys
- **Auto-Detection**: Automatically detects whether to use CharField or IntegerField based on choice keys

## Installation

Install from PyPI:

```bash
pip install django-metachoices
# or with UV (recommended)
uv add django-metachoices
```

That's it! No need to add anything to `INSTALLED_APPS` - just import and use the field directly in your models.

## Requirements

- **Python**: 3.10+
- **Django**: 4.2+



## Compatibility

This package is tested with:
- **Python**: 3.10, 3.11, 3.12, 3.13
- **Django**: 4.2 (LTS), 5.0, 5.1, 5.2

For local testing across multiple versions, we recommend using `tox`:

```bash
# Install development dependencies
uv add --group dev tox

# Test specific combinations
uv run tox -e py310-django42    # Python 3.10 + Django 4.2
uv run tox -e py312-django51    # Python 3.12 + Django 5.1
uv run tox -e py313-django52    # Python 3.13 + Django 5.2

# Test with multiple Python versions (requires installing them first)
uv python install 3.10 3.11 3.12 3.13
uv run tox
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 