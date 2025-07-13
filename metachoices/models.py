from django.db import models

from .fields import MetaChoiceField

META_CHOICES = {
    "DB1": {
        "display": "Database 1",
        "description": "Primary database for storing user data.",
        "url": "https://db1.example.com",
        "icon": "db1_icon.png",
    },
    "DB2": {
        "display": "Database 2",
        "description": "Secondary database for backup and redundancy.",
        "url": "https://db2.example.com",
        "icon": "db2_icon.png",
    },
    "DB3": {
        "display": "Database 3",
        "description": "Third database for specialized data storage.",
        "url": "https://db3.example.com",
        "icon": "db3_icon.png",
    },
}

META_CHOICES_2 = {
    1: {
        "display": "One",
    },
    2: {
        "display": "Two",
    },
    3: {
        "display": "Three",
    },
}


class Storage(models.Model):
    """Model to represent different database storage options."""

    database = MetaChoiceField(
        choices=META_CHOICES,
        verbose_name="Database Storage",
        help_text="Select the database for storage.",
    )
    count = MetaChoiceField(
        choices=META_CHOICES_2,
        verbose_name="Count",
        help_text="Select a count option.",
        null=True,
        blank=True,
    )
