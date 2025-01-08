from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    """"
    Model representing a category of inventory items
    Categories can have parent-child relationships, allowing hierarchical categorization.
    """

    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']  # Order categories alphabetically by name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.parent_category:
            # If it has a parent category, it's a subcategory
            return reverse("inventory-subcategory-list", args=[self.parent_category.slug, self.slug])
        else:
            # If it has no parent category, it's a main category
            return reverse("inventory-category-list", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto-generate a slug if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class InventoryItem(models.Model):
    """ 
    Model representing an inventory item.
    Items belong to categories and can optionally include details like location, serial numbers, and specifications.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    can_be_loaned = models.BooleanField(default=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    mac_address = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(
        upload_to="inventory-images", null=True, blank=True)
    official_link = models.URLField(null=True, blank=True)
    specs = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def __str__(self):
        """
        Returns a string representation of the item, including its name, location, and category.
        """
        return f"{self.name} - {self.location} / {self.category}"

    def get_absolute_url(self):
        """
        Returns the URL to access the detail page of this item.
        """
        return reverse("inventory-category-list", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto-generate a slug if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
