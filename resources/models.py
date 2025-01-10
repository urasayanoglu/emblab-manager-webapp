from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class ResourceCategory(models.Model):
    """
    Model representing the category of a resource or a subcategory, e.g. Programming Languages or Python.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text="Name of the resource category.")
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories', help_text="Parent category for creating subcategories, Optional if the category is a top-level category.")
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    class Meta:
        verbose_name = "Resource Category"
        verbose_name_plural = "Resource Categories"
        ordering = ['name']  # Alphabetical ordering by default

    def __str__(self):
        """
        String representation of the ResourceCategory object.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL for the ResourceCategory object.
        """
        return reverse("resource-category", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Auto-generate the slug from the name if it is not already set.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Resource(models.Model):
    """
    Model representing a learning resource related to embedded software and systems.
    """
    title = models.CharField(
        max_length=100, help_text="Title of the resource.")
    category = models.ForeignKey(
        ResourceCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Category under which the resource falls.")
    type = models.CharField(max_length=100, choices=[
        ('Video', 'Video'),
        ('Blog', 'Blog'),
        ('Book', 'Book'),
        ('Article', 'Article'),
        ('Course', 'Course'),
        ('Tutorial', 'Tutorial'),
        ('Documentation', 'Documentation'),
        ('Other', 'Other'),
    ], help_text="Type of the resource (e.g., Video, Blog, etc.)")
    link = models.URLField(null=True, blank=True)
    description = models.TextField(
        null=True, blank=True, help_text="Brief description of the resource.")
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    class Meta:
        ordering = ['title']  # Alphabetical ordering by default

    def __str__(self):
        """
        String representation of the Resource object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL for the Resource object.
        """
        return reverse("resource-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
