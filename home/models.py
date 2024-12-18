from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Data models for the home application


class Announcement(models.Model):
    """
    Model representing an announcement.

    Attributes:
        title (str): The title of the announcement.
        date (date): The date of the announcement. Optional.
        description (str): A detailed description of the announcement. Optional.
        slug (str): A URL-friendly version of the title, automatically generated if not provided.
    """
    title = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def __str__(self):
        """
        Returns the string representation of the announcement, which is its title.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL for the announcement detail page.
        """
        return reverse("announcement-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a slug from the title
        if no slug is provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
