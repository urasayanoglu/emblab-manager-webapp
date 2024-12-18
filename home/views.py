from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, BackgroundImage
from .forms import FeedbackForm
from django.contrib import messages


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


def feedback_view(request):
    """
    Handles the submission and display of the feedback form.

    If the request is a POST request, the function validates the submitted form.
    If valid, the feedback is saved, and the user is redirected to the About page
    with a success message. For GET requests, the form is displayed, pre-filled
    with the user's name and email if they are logged in.

    Args:
        request (HttpRequest): The HTTP request object.

    Template:
        home/feedback.html

    Context:
        form (FeedbackForm): The feedback form instance, either blank or pre-filled.
    """
    if request.method == 'POST':
        # Instantiate the form with POST data and the current user.
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            # Save the feedback to the database
            form.save()
            # Add a success message to notify the user
            messages.success(request, 'Thank you for your feedback!')
            # Redirect the user to the about page after submission
            return redirect('about')
    else:
        # Pre-fill form if the user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                # User model has `first_name` and `last_name` ; it comes from Django's built-in User model
                'name': request.user.get_full_name(),  # Combines first_name and last_name
                'email': request.user.email,  # Prefills email from the user's profile
            }
        # Instantiate the form with initial data and the current user
        form = FeedbackForm(initial=initial_data, user=request.user)
    # Render the feedback form template with the form context
    return render(request, 'home/feedback.html', {'form': form})
