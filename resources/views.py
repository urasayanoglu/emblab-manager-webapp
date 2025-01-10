from django.shortcuts import render, get_object_or_404
from .models import ResourceCategory, Resource


def resource_list(request):
    """
    View to display the list of resouce categories, subcategories, and resources.
    Handles category navigation and resource detail view.
    """
    # Get all top-level categories (categories without parent categories)
    categories = ResourceCategory.objects.filter(parent_category__isnull=True)

    # Retrieve selected category slug and resource id from the request
    selected_category_slug = request.GET.get('category', None)
    selected_resource_id = request.GET.get('resource', None)

    # Initialize variables for selected data
    selected_category = None
    resources = None
    selected_resource = None
    subcategories = []

    # Handle category navigation
    if selected_category_slug:
        selected_category = get_object_or_404(
            ResourceCategory, slug=selected_category_slug)
        subcategories = ResourceCategory.objects.filter(
            parent_category=selected_category)

        # If no subcategories exist, list resources under the selected category
        if not subcategories.exists():
            resources = Resource.objects.filter(category=selected_category)

    # Handle resource detail view
    if selected_resource_id:
        selected_resource = get_object_or_404(
            Resource, id=selected_resource_id)
        if selected_category_slug:
            selected_category = get_object_or_404(
                ResourceCategory, slug=selected_category_slug)
            subcategories = ResourceCategory.objects.filter(
                parent_category=selected_category)
            resources = Resource.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'resources': resources,
        'selected_resource': selected_resource,
        'selected_category': selected_category,
    }
    return render(request, 'resources/resource-index.html', context)
