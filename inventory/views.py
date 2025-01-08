from django.shortcuts import render, get_object_or_404
from .models import InventoryItem, Category

def inventory_list(request):
    """
    Display the inventory list with category navigation, search functionality, 
    and detailed item view.

    - Top-level categories are shown by default.
    - Users can navigate subcategories, search for items, or view item details.
    """
    # Get all top-level categories (i.e., categories without parent categories)
    categories = Category.objects.filter(parent_category__isnull=True)

    # Retrieve selected category slug and search query from the request
    selected_category_slug = request.GET.get('category', None)
    search_query = request.GET.get('search', None)
    
    # Initialize empty results and variables
    items = InventoryItem.objects.none()  # Start with an empty queryset
    subcategories = []
    selected_category = None # Currently selected category
    selected_item = None # Currently selected item for detailed view

    # Handle category navigation
    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        subcategories = Category.objects.filter(parent_category=selected_category)

        # If no subcategories exist, list items under the selected category
        if not subcategories.exists():
            items = InventoryItem.objects.filter(category=selected_category)

    # Handle search queries
    if search_query:
        search_query = search_query.strip()  # Remove any extra spaces
        # Search items by name and also look for items in categories that match the search query
        categories_matching = Category.objects.filter(name__icontains=search_query)
        items_by_name = InventoryItem.objects.filter(name__icontains=search_query)
        items_by_category = InventoryItem.objects.filter(category__in=categories_matching)
        # Combine both querysets (item name and category matches)
        items = items_by_name.union(items_by_category)


    # Handle selected item for detailed view
    item_id = request.GET.get('item')
    if item_id:
        selected_item = get_object_or_404(InventoryItem, id=item_id)

    context = {
        "categories": categories,
        "subcategories": subcategories,
        "items": items,
        "selected_item": selected_item,
        "search_query": search_query,
        "selected_category": selected_category,
    }

    return render(request, 'inventory/inventory-index.html', context)

def inventory_subcategory_list(request, parent_slug, subcategory_slug):
    """
    Display items in a specific subcategory under a given parent category.

    Args:
        request: The HTTP request object.
        parent_slug: The slug of the parent category.
        subcategory_slug: The slug of the subcategory.

    Returns:
        Rendered template with items in the specified subcategory.
    """
    # Get parent and subcategory by their slugs
    parent_category = get_object_or_404(Category, slug=parent_slug)
    subcategory = get_object_or_404(Category, slug=subcategory_slug, parent_category=parent_category)

    # Get items under this subcategory
    items = InventoryItem.objects.filter(category=subcategory)

    context = {
        "parent_category": parent_category,
        "subcategory": subcategory,
        "items": items,
    }
    return render(request, 'inventory/inventory-index.html', context)

def inventory_category_detail(request, category_slug):
    """
    Display details and items of a specific category.

    Args:
        request: The HTTP request object.
        category_slug: The slug of the category.

    Returns:
        Rendered template with category details and items.
    """
    category = get_object_or_404(Category, slug=category_slug)

    # Get items under this category
    items = InventoryItem.objects.filter(category=category)

    context = {
        "category": category,
        "items": items,
    }
    return render(request, 'inventory/inventory-index.html', context)
