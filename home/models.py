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


class BackgroundImage(models.Model):
    """
    Model representing a background image for the landing page.

    Attributes:
        image (ImageField): The uploaded background image file.
        description (str): A short description of the image. Optional.
    """
    image = models.ImageField(upload_to='images/home-images/')
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the background image, which is its description.
        If no description is provided, returns a placeholder text.
        """
        return self.description if self.description else "Background Image"

    class Meta:
        """
        Metadata for the BackgroundImage model.

        Attributes:
            verbose_name (str): The singular name of the model, used in the Django admin interface.
            verbose_name_plural (str): The plural name of the model, used in the Django admin interface.
        """
        verbose_name = "Background Image"
        verbose_name_plural = "Background Images"


class UserFeedback(models.Model):
    """
    Model representing feedback provided by users.

    Attributes:
        name (str): The name of the user providing the feedback. Optional.
        email (str): The email address of the user. Optional.
        message (str): The feedback message provided by the user. Required.
        created_at (datetime): The timestamp when the feedback was created. Automatically set when a feedback entry is created.
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the feedback.
        If the user's name is not provided, 'Anonymous' is used instead.
        """
        return f"Feedback from {self.name or 'Anonymous'} on {self.created_at.strftime('%d-%m-%Y')}"

    class Meta:
        """
        Metadata for the UserFeedback model.

        Attributes:
            verbose_name (str): The singular name of the model, used in the Django admin interface.
            verbose_name_plural (str): The plural name of the model, used in the Django admin interface.
        """
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedback"
