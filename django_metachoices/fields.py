from django.db import models

from .mixins import MetaChoiceMixin


class IntegerMetaChoiceField(MetaChoiceMixin, models.IntegerField):
    """An IntegerField with meta choices functionality."""

    def __init__(self, *args, **kwargs):
        """Initialize the integer field with choices."""
        super().__init__(*args, **kwargs)
        # Ensure choices is never None
        if not hasattr(self, 'choices') or self.choices is None:
            self.choices = []

    def formfield(self, **kwargs):
        """Return the appropriate form field for integer choices."""
        from django import forms

        defaults = {"form_class": forms.TypedChoiceField, "coerce": int}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CharMetaChoiceField(MetaChoiceMixin, models.CharField):
    """A CharField with meta choices functionality."""

    def __init__(self, *args, **kwargs):
        """Set default max_length for char fields."""
        kwargs.setdefault("max_length", 100)
        super().__init__(*args, **kwargs)
        # Ensure choices is never None
        if not hasattr(self, 'choices') or self.choices is None:
            self.choices = []


class MetaChoiceField(models.Field):
    """A custom field to store meta choices with additional metadata.

    Automatically detects whether to behave as IntegerField or CharField
    based on the data types of the meta_choices keys.

    This class serves as a factory that returns the appropriate field type.
    """

    def __new__(cls, *args, choices=None, **kwargs):
        """Create the appropriate field instance based on choice key types."""
        if choices:
            if isinstance(choices, dict):
                # Check the type of the first key to determine field type
                sample_key = next(iter(choices.keys()))
                if isinstance(sample_key, int):
                    return IntegerMetaChoiceField(*args, choices=choices, **kwargs)
            elif isinstance(choices, list | tuple):
                # Standard Django format: [(key, display), ...]
                if choices:
                    sample_key = choices[0][0]
                    if isinstance(sample_key, int):
                        return IntegerMetaChoiceField(*args, choices=choices, **kwargs)

        # Default to CharField for string keys or when no choices provided
        return CharMetaChoiceField(*args, choices=choices, **kwargs)
