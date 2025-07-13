"""Tests for django-metachoices package."""

import pytest
from django import forms
from django.db import models

from django_metachoices import MetaChoiceField
from django_metachoices.models import META_CHOICES, META_CHOICES_2, Storage


@pytest.mark.django_db
def test_meta_choices_basic_functionality():
    """Test basic accessing of MetaChoiceField data."""
    # Create a storage instance with a valid choice
    storage = Storage.objects.create(database="DB1")

    assert storage.database == "DB1"
    assert storage.get_database_display() == "Database 1"
    assert (
        storage.get_database_description() == "Primary database for storing user data."
    )
    assert storage.get_database_url() == "https://db1.example.com"
    assert storage.get_database_icon() == "db1_icon.png"


@pytest.mark.django_db
def test_meta_choices_all_options():
    """Test that all META_CHOICES options work correctly."""
    # Test DB2
    storage2 = Storage.objects.create(database="DB2")
    assert storage2.get_database_display() == "Database 2"
    assert (
        storage2.get_database_description()
        == "Secondary database for backup and redundancy."
    )
    assert storage2.get_database_url() == "https://db2.example.com"
    assert storage2.get_database_icon() == "db2_icon.png"

    # Test DB3
    storage3 = Storage.objects.create(database="DB3")
    assert storage3.get_database_display() == "Database 3"
    assert (
        storage3.get_database_description()
        == "Third database for specialized data storage."
    )
    assert storage3.get_database_url() == "https://db3.example.com"
    assert storage3.get_database_icon() == "db3_icon.png"


@pytest.mark.django_db
def test_meta_choices_invalid_value():
    """Test behavior with invalid choice values."""
    # Create storage with invalid choice
    # (should be allowed by Django but getter methods should return None)
    storage = Storage(database="INVALID")

    # This should work as Django doesn't validate choices on save by default
    storage.save()

    assert storage.database == "INVALID"
    # get_display should return the raw value for invalid choices (Django behavior)
    assert storage.get_database_display() == "INVALID"
    # Other getters should return None for invalid choices
    assert storage.get_database_description() is None
    assert storage.get_database_url() is None
    assert storage.get_database_icon() is None


@pytest.mark.django_db
def test_meta_choices_empty_value():
    """Test behavior with empty choice values."""
    storage = Storage(database="")
    storage.save()

    assert storage.database == ""
    assert storage.get_database_display() == ""
    assert storage.get_database_description() is None
    assert storage.get_database_url() is None
    assert storage.get_database_icon() is None


def test_meta_choices_field_validation():
    """Test that MetaChoiceField validates choices properly."""
    # Test with valid meta choices
    field = MetaChoiceField(choices=META_CHOICES)
    assert field.choices == [
        ("DB1", "Database 1"),
        ("DB2", "Database 2"),
        ("DB3", "Database 3"),
    ]

    # Test with standard Django choices
    standard_choices = [("A", "Option A"), ("B", "Option B")]
    field2 = MetaChoiceField(choices=standard_choices)
    assert field2.choices == standard_choices


def test_meta_choices_dynamic_attributes():
    """Test that dynamic attributes are created correctly."""
    # Create a test model with meta choices
    class DynamicAttributesTestModel(models.Model):
        choice_field = MetaChoiceField(choices=META_CHOICES)

        class Meta:
            app_label = "django_metachoices"

    # Check that getter methods exist
    test_instance = DynamicAttributesTestModel(choice_field="DB1")
    assert hasattr(test_instance, "get_choice_field_display")
    assert hasattr(test_instance, "get_choice_field_description")
    assert hasattr(test_instance, "get_choice_field_url")
    assert hasattr(test_instance, "get_choice_field_icon")


def test_meta_choices_with_missing_attributes():
    """Test behavior when choices have missing attributes."""
    incomplete_choices = {
        "A": {"display": "Option A", "description": "Description A"},
        "B": {"display": "Option B"},  # Missing description
        "C": {"display": "Option C", "description": "Description C", "extra": "Extra C"},
    }

    class MissingAttributesTestModel(models.Model):
        choice_field = MetaChoiceField(choices=incomplete_choices)

        class Meta:
            app_label = "django_metachoices"

    # Test with choice that has all attributes
    test_a = MissingAttributesTestModel(choice_field="A")
    assert test_a.get_choice_field_display() == "Option A"
    assert test_a.get_choice_field_description() == "Description A"
    assert test_a.get_choice_field_extra() is None

    # Test with choice that has missing attributes
    test_b = MissingAttributesTestModel(choice_field="B")
    assert test_b.get_choice_field_display() == "Option B"
    assert test_b.get_choice_field_description() is None
    assert test_b.get_choice_field_extra() is None

    # Test with choice that has extra attributes
    test_c = MissingAttributesTestModel(choice_field="C")
    assert test_c.get_choice_field_display() == "Option C"
    assert test_c.get_choice_field_description() == "Description C"
    assert test_c.get_choice_field_extra() == "Extra C"


def test_meta_choices_field_without_meta_choices():
    """Test MetaChoiceField without meta_choices parameter."""
    field = MetaChoiceField(max_length=50)
    assert field.choices == []

    # Should work like a regular CharField
    class NoChoicesTestModel(models.Model):
        choice_field = MetaChoiceField(max_length=50)

        class Meta:
            app_label = "django_metachoices"

    test_instance = NoChoicesTestModel(choice_field="test")
    assert test_instance.choice_field == "test"


def test_meta_choices_custom_attributes():
    """Test with custom attributes in meta choices."""
    custom_choices = {
        "RED": {
            "display": "Red Color",
            "hex": "#FF0000",
            "rgb": (255, 0, 0),
            "is_primary": True,
        },
        "BLUE": {
            "display": "Blue Color",
            "hex": "#0000FF",
            "rgb": (0, 0, 255),
            "is_primary": True,
        },
    }

    class CustomTestModel(models.Model):
        option = MetaChoiceField(choices=custom_choices)

        class Meta:
            app_label = "django_metachoices"

    test_instance = CustomTestModel(option="RED")
    assert test_instance.get_option_display() == "Red Color"
    assert test_instance.get_option_hex() == "#FF0000"
    assert test_instance.get_option_rgb() == (255, 0, 0)
    assert test_instance.get_option_is_primary() is True


def test_meta_choices_field_inheritance():
    """Test that MetaChoiceField works with model inheritance."""
    
    class BaseModel(models.Model):
        base_choice = MetaChoiceField(choices=META_CHOICES)

        class Meta:
            app_label = "django_metachoices"
            abstract = True

    class ChildModel(BaseModel):
        child_field = models.CharField(max_length=100)

        class Meta:
            app_label = "django_metachoices"

    child_instance = ChildModel(base_choice="DB1", child_field="test")
    assert child_instance.get_base_choice_display() == "Database 1"
    assert child_instance.get_base_choice_description() == "Primary database for storing user data."


def test_meta_choices_field_with_standard_django_options():
    """Test MetaChoiceField with standard Django field options."""
    field = MetaChoiceField(
        choices=META_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        default="DB1",
        help_text="Choose a database",
        verbose_name="Database Choice",
    )

    assert field.max_length == 50
    assert field.blank is True
    assert field.null is True
    assert field.default == "DB1"
    assert field.help_text == "Choose a database"
    assert field.verbose_name == "Database Choice"


def test_meta_choices_field_integer():
    """Test MetaChoiceField with integer choices."""
    meta_choices = {
        1: {"display": "First", "order": 1},
        2: {"display": "Second", "order": 2},
        3: {"display": "Third", "order": 3},
    }

    class IntegerMetaChoiceFieldTestModel(models.Model):
        choice = MetaChoiceField(choices=meta_choices, default=1)

        class Meta:
            app_label = "django_metachoices"

    # Test field creation and getter methods without database
    test_instance = IntegerMetaChoiceFieldTestModel(choice=2)
    assert test_instance.choice == 2
    assert test_instance.get_choice_display() == "Second"
    assert test_instance.get_choice_order() == 2


@pytest.mark.django_db
def test_meta_choices_2_with_form():
    """Test MetaChoiceField with forms."""
    storage = Storage.objects.create(database="DB1", count=2)

    class StorageForm(forms.ModelForm):
        class Meta:
            model = Storage
            fields = ["database", "count"]

    form = StorageForm(instance=storage)
    assert form.initial["database"] == "DB1"
    assert form.initial["count"] == 2

    # Test form validation
    form_data = {"database": "DB2", "count": 3}
    form = StorageForm(data=form_data)
    assert form.is_valid()

    if form.is_valid():
        instance = form.save(commit=False)
        assert instance.database == "DB2"
        assert instance.count == 3 