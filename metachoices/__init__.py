"""Django Meta Choices - Rich metadata for Django choice fields."""

from .fields import CharMetaChoiceField, IntegerMetaChoiceField, MetaChoiceField
from .mixins import MetaChoiceMixin

__version__ = "0.1.2"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "MetaChoiceField",
    "CharMetaChoiceField",
    "IntegerMetaChoiceField",
    "MetaChoiceMixin",
]

# Default Django app configuration
default_app_config = "metachoices.apps.MetachoicesConfig"
