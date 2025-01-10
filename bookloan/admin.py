from django.contrib import admin
from .models import Table, TableBooking, LoanItem

# Register your models here.


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tables.
    """
    list_filter = ("number", "location", "capacity", "is_active")
    list_display = ("number", "location", "capacity", "is_active")
    search_fields = ("number", "location", "capacity")
    ordering = ["number"]


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    """
    Admin interface for managing table bookings.
    """
    list_filter = ("table", "is_confirmed", "booking_start", "booking_end")
    list_display = ("table_number", "user", "booking_start",
                    "booking_end", "is_confirmed")
    search_fields = ("table__number", "user__username",
                     "booking_start", "booking_end")
    date_hierarchy = "booking_start"
    ordering = ["-booking_start"]
    # Allow editing the 'is_confirmed' status directly in the list view
    list_editable = ("is_confirmed",)

    def table_number(self, obj):
        """
        Custom display for the table number associated with a booking.
        """
        return obj.table.number
    table_number.short_description = "Table Number"


@admin.register(LoanItem)
class LoanItemAdmin(admin.ModelAdmin):
    """
    Admin interface for managing loaned items.
    """
    list_filter = ("item", "user", "loan_start", "return_due",
                   "is_returned", "is_confirmed")
    list_display = ("item_name", "user", "loan_start",
                    "return_due", "is_returned", "is_confirmed")
    search_fields = ("item__name", "user__username",
                     "loan_start", "return_due")
    list_editable = ("is_returned", "is_confirmed")
    date_hierarchy = "loan_start"
    ordering = ["-loan_start"]

    def item_name(self, obj):
        """
        Custom display for the name of the loaned item.
        """
        return obj.item.name
    item_name.short_description = "Item Name"
