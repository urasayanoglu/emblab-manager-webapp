from django.shortcuts import render, get_object_or_404
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


def announcement_detail(request, slug):
    """
        Renders the detail page for a specific announcement.

        Fetches an announcement based on the provided slug. If no matching
        announcement is found, a 404 error is raised.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the announcement to fetch.

        Context:
            announcement (Announcement): The announcement object to display.

        Template:
            home/announcement-detail.html
        """
    # Fetch the announcement using the slug or return a 404 if not found.
    announcement = get_object_or_404(Announcement, slug=slug)

    # Render the announcement detail page with the fetched announcement.
    return render(request, 'home/announcement-detail.html', {'announcement': announcement})


def about(request):
    """
    Renders the About page of the TUAS Embedded Lab Manager.

    The About page provides an overview of the application, its features,
    and guidance on how to use its functionalities. It is accessible via the
    navigation bar by clicking the name of the web application.

    Args:
        request (HttpRequest): The HTTP request object.

    Template:
        home/about.html
    """
    # Render the about page template.
    return render(request, 'home/about.html')
