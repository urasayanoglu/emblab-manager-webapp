from django.contrib import admin
from . models import InventoryItem, Category

# Register your models here.


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the InventoryItem model.
    Provides filters, search fields, and a prepopulated slug field in the admin interface.
    """
    list_filter = ("category", "quantity", "location")
    list_display = ("name", "category", "location",
                    "serial_number", "mac_address", "quantity")
    search_fields = ("name", "serial_number", "mac_address", "location")
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    Includes search fields, filters, and a prepopulated slug field for better admin usability.
    """
    list_display = ("name", "parent_category")
    search_fields = ("name",)  # Adding search fields for categories
    list_filter = ("parent_category",)  # Adding filter by parent category
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Category, CategoryAdmin)
