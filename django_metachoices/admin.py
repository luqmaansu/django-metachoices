from django.contrib import admin

from .models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    """Admin interface for Storage model."""

    list_display = ["database", "get_database_display", "get_database_description"]
    list_filter = ["database"]
    search_fields = ["database"]

    def get_database_description(self, obj):
        """Display the database description in admin."""
        return obj.get_database_description()

    get_database_description.short_description = "Description"

    def get_database_display(self, obj):
        """Display the database display name in admin."""
        return obj.get_database_display()

    get_database_display.short_description = "Display Name"
