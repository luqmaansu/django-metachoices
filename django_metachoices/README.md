# Django Meta Choices

A Django field extension that allows choices to have rich metadata beyond the standard (value, display) tuple.

## Overview

Django's standard choice fields only support a simple key-value mapping. This package extends that functionality to allow arbitrary metadata for each choice, which can be accessed through dynamically generated getter methods.

## Features

- **Rich Metadata**: Add any number of attributes to your choices (description, url, icon, priority, etc.)
- **Dynamic Getters**: Automatically generates `get_<field>_<attribute>()` methods for all metadata attributes
- **Django Compatible**: Works seamlessly with Django's existing choice field functionality
- **Admin Integration**: Fully compatible with Django admin
- **Type Safe**: Validates that field values are valid choice keys

## Installation

Add the `django_metachoices` app to your Django project's `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_metachoices',
]
```

## Usage

### Basic Example

```python
from django.db import models
from django_metachoices.models import MetaChoiceField

# Define your choices with metadata
DATABASE_CHOICES = {
    "MYSQL": {
        "display": "MySQL Database",
        "description": "Open-source relational database",
        "url": "https://mysql.com",
        "icon": "mysql-icon.png",
        "port": 3306,
        "supports_transactions": True,
    },
    "POSTGRES": {
        "display": "PostgreSQL Database",
        "description": "Advanced open-source relational database",
        "url": "https://postgresql.org",
        "icon": "postgres-icon.png",
        "port": 5432,
        "supports_transactions": True,
    },
    "REDIS": {
        "display": "Redis Cache",
        "description": "In-memory data structure store",
        "url": "https://redis.io",
        "icon": "redis-icon.png",
        "port": 6379,
        "supports_transactions": False,
    }
}

class DatabaseConfig(models.Model):
    database_type = MetaChoiceField(
        meta_choices=DATABASE_CHOICES,
        verbose_name="Database Type",
        help_text="Select the database type for this configuration"
    )
```

### Accessing Metadata

```python
# Create an instance
config = DatabaseConfig.objects.create(database_type="POSTGRES")

# Access the stored value
print(config.database_type)  # "POSTGRES"

# Access metadata through dynamic getters
print(config.get_database_type_display())              # "PostgreSQL Database"
print(config.get_database_type_description())          # "Advanced open-source relational database"
print(config.get_database_type_url())                  # "https://postgresql.org"
print(config.get_database_type_icon())                 # "postgres-icon.png"
print(config.get_database_type_port())                 # 5432
print(config.get_database_type_supports_transactions()) # True
```

### Custom Attributes

You can add any attributes you need:

```python
STATUS_CHOICES = {
    "ACTIVE": {
        "display": "Active",
        "color": "#28a745",
        "priority": 1,
        "can_edit": True,
        "notification_settings": {
            "email": True,
            "sms": False
        }
    },
    "INACTIVE": {
        "display": "Inactive",
        "color": "#dc3545",
        "priority": 3,
        "can_edit": False,
        "notification_settings": {
            "email": False,
            "sms": False
        }
    }
}

class UserStatus(models.Model):
    status = MetaChoiceField(meta_choices=STATUS_CHOICES)

# Usage
user_status = UserStatus.objects.create(status="ACTIVE")
print(user_status.get_status_color())                    # "#28a745"
print(user_status.get_status_priority())                 # 1
print(user_status.get_status_can_edit())                 # True
print(user_status.get_status_notification_settings())    # {"email": True, "sms": False}
```

## Field Options

`MetaChoiceField` supports all standard Django `CharField` options:

```python
class MyModel(models.Model):
    my_field = MetaChoiceField(
        meta_choices=MY_CHOICES,
        max_length=50,           # Custom max length (default: 100)
        blank=True,              # Allow blank values
        null=True,               # Allow null values
        default="DEFAULT_KEY",   # Default choice
        help_text="Choose an option",
        verbose_name="My Field"
    )
```

## Django Admin Integration

The field works seamlessly with Django admin:

```python
from django.contrib import admin
from .models import DatabaseConfig

@admin.register(DatabaseConfig)
class DatabaseConfigAdmin(admin.ModelAdmin):
    list_display = ['database_type', 'get_database_type_display', 'get_database_type_description']
    list_filter = ['database_type']

    def get_database_type_description(self, obj):
        return obj.get_database_type_description()
    get_database_type_description.short_description = 'Description'
```

## Error Handling

- **Invalid Values**: If a field contains a value not in `meta_choices`, `get_<field>_display()` returns the raw value (Django's default behavior), while other getters return `None`
- **Missing Attributes**: If a choice doesn't have a specific attribute, the getter returns `None`
- **Empty Choices**: The field works without `meta_choices` parameter, behaving like a standard `CharField`

## Testing

The package includes comprehensive tests covering:

- Basic functionality
- All choice options
- Invalid and empty values
- Dynamic attribute creation
- Custom attributes
- Field inheritance
- Django integration

Run tests with:
```bash
pytest django_metachoices/tests.py
```

## Implementation Details

The `MetaChoiceField` uses Django's `contribute_to_class()` method to dynamically add getter methods to the model class during initialization. This follows the same pattern Django uses for its built-in `get_FOO_display()` method.

Key features:
- No model mixins required
- Pure field-based implementation
- Follows Django conventions
- Backward compatible with standard choice fields

## Requirements

- Django 3.2+
- Python 3.8+

## License

This package is released under the MIT License.
