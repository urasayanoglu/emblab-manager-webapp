from django.urls import path
from . import views

# Define URL patterns for the home application
urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("announcement/<slug:slug>/", views.announcement_detail,
         name="announcement-detail"),  # Announcement detail page
    path("about/", views.about, name="about"),  # About page
    path("feedback/", views.feedback_view, name="feedback"),  # Feedback page
]
