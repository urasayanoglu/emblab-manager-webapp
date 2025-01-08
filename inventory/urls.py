from django.urls import path
from . import views


urlpatterns = [
    # URL for listing top-level categories
    path("", views.inventory_list, name="inventory-category-list"),

    # URL for listing subcategories of a given category
    path("<slug:parent_slug>/<slug:subcategory_slug>/", views.inventory_subcategory_list, name="inventory-subcategory-list"),

    # URL for displaying items in a category
    path("<slug:category_slug>/", views.inventory_category_detail, name="inventory-category-detail"),
]