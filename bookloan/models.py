from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import InventoryItem
from django.core.exceptions import ValidationError


class Table(models.Model):
    """Model representing a table in the lab."""
    number = models.PositiveIntegerField(
        unique=True, help_text="Unique table number in the lab.")
    location = models.CharField(
        max_length=50, blank=True, null=True, help_text="Location of the table in the lab.")
    capacity = models.PositiveIntegerField(
        help_text="Maximum number of people the table can accommodate.")
    # Additional description if needed
    description = models.CharField(
        max_length=200, blank=True, null=True, help_text="Additional details about the table.")
    is_active = models.BooleanField(
        default=True, help_text="Indicates if the table is available for booking.")
    bookable_start_time = models.TimeField(
        default='08:00', help_text="Earliest time the table can be booked.")
    bookable_end_time = models.TimeField(
        default='18:00', help_text="Latest time the table can be booked.")

    class Meta:
        ordering = ['number']
        verbose_name = "Lab Table"
        verbose_name_plural = "Lab Tables"

    def __str__(self):
        """String for representing the Table object."""
        return f"Table {self.number}"

    def get_absolute_url(self):
        """Returns the URL for accessing details of this table."""
        return reverse("table-detail", args=[str(self.id)])


class TableBooking(models.Model):
    """Model representing a table booking in the lab"""
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, help_text="The table being booked.")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who is booking the table.")
    booking_start = models.DateTimeField(
        help_text="Start date and time of the booking.")
    booking_end = models.DateTimeField(
        help_text="End date and time of the booking.")
    is_confirmed = models.BooleanField(
        default=True, help_text="Indicates if the booking has been confirmed by the admin.")

    class Meta:
        # To prevent double booking of the same table at the same time
        unique_together = ('table', 'booking_start', 'booking_end')
        ordering = ['-booking_start']
        verbose_name = "Table Booking"
        verbose_name_plural = "Table Bookings"

    def __str__(self):
        """String for representing the TableBooking object."""
        return f"{self.table} booked by {self.user.username} from {self.booking_start} to {self.booking_end}"

    def get_absolute_url(self):
        return reverse("table-booking-detail", args=[str(self.id)])

    def clean(self):
        """Custom validation to ensure bookings are within the allowed times."""
        if self.booking_start.time() < self.table.bookable_start_time or self.booking_end.time() > self.table.bookable_end_time:
            raise ValidationError(f"Booking times must be between {
                                  self.table.bookable_start_time} and {self.table.bookable_end_time}")


class LoanItem(models.Model):
    """Model representing a loan of an item"""
    item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, help_text="The item being loaned.")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who is loaning the item.")
    loan_start = models.DateField(help_text="Date when the loan starts.")
    return_due = models.DateField(
        help_text="Date when the item must be returned.")
    is_returned = models.BooleanField(
        default=False, help_text="Indicates if the item has been returned.")
    is_confirmed = models.BooleanField(
        default=False, help_text="Indicates if the loan has been confirmed by the admin.")

    class Meta:
        ordering = ['return_due']
        verbose_name = "Loan Item"
        verbose_name_plural = "Loan Items"

    def __str__(self):
        """String for representing the LoanItem object."""
        return f"{self.item.name} loaned by {self.user.username} (Due: {self.return_due})"

    def get_absolute_url(self):
        """Returns the URL for accessing details of this loan."""
        return reverse("loan-item-detail", args=[str(self.id)])

    # Uncomment and customize the following code if you wish to automatically update inventory quantity upon loan creation.
    # For now quantity incrementing and decrementing is handled in the bookloan_view() function in views.py
    """def save(self, *args, **kwargs):
        # Automatically update inventory quantity upon loan creation
        if not self.is_returned:
            self.item.quantity -= 1
            self.item.save()
        super().save(*args, **kwargs)"""
