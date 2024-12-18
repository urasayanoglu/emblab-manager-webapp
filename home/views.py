from django.shortcuts import render
from .models import Announcement, BackgroundImage


def home(request):
    """
    Renders the home page of the application.

    Fetches the latest announcements and all background images to be displayed
    on the home page.

    Context:
        announcements (QuerySet): The latest 5 announcements ordered by date in descending order.
        background_images (QuerySet): All background images for the home page.

    Template:
        home/home.html
    """
    # Fetch latest 5 announcements ordered by date in descending order.
    announcements = Announcement.objects.order_by('-date')[:5]

    # Fetch all background images for the home page.
    background_images = BackgroundImage.objects.all()

    # Render the home page with the context data.
    return render(request, 'home/home.html', {
        'announcements': announcements,
        'background_images': background_images,
    })
