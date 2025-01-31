from django.contrib import admin
from .models import ResourceCategory, Resource


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for ResourceCategory.
    """
    list_display = (
        "name", "parent_category")  # Display name and parent category
    search_fields = ("name",)  # Enable search by name
    list_filter = ("parent_category",)  # Add filter by parent category
    # Automatically populate slug field
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Resource.
    """
    list_display = ("title", "category",
                    "type", "link")  # Display title, category, and type
    # Enable search by title and description
    search_fields = ("title", "description", "link")
    list_filter = ("category", "type")  # Add filters for category and type
    # Automatically populate slug field
    prepopulated_fields = {"slug": ("title",)}
