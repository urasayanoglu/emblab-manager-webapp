from django.contrib import admin
from .models import Announcement, BackgroundImage, UserFeedback

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Announcement model.
    """
    
    list_display = ('title', 'date', 'slug') # Display these fields in the admin list view
    list_filter = ('date',)  # Add a filter sidebar for the date field
    search_fields = ('title', 'description')  # Enable search by title and description  
    prepopulated_fields = {'slug': ('title',)} # Automatically generate the slug from the title
    ordering = ('-date',)  # Order announcements by the most recent date

@admin.register(BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the BackgroundImage model.
    """
    list_display = ('description', 'image')  # Show description and image fields in the admin list view
    search_fields = ('description',)  # Enable search by description


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the UserFeedback model.
    """
    list_display = ('name', 'email', 'created_at')  # Display these fields in the admin list view
    list_filter = ('created_at',)  # Add a filter sidebar for feedback creation dates
    search_fields = ('name', 'email', 'message')  # Enable search by name, email, and message
    ordering = ('-created_at',)  # Order feedback by the most recent submission

