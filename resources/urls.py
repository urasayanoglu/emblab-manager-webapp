from django.urls import path
from . import views

urlpatterns = [
    # Main resource index page
    path('', views.resource_list, name='resource-index'),
    # Category-specific resource list
    path('category/<slug:category_slug>/',
         views.resource_list, name='resource-category'),
    # Resource detail page
    path('resource/<int:resource_id>/',
         views.resource_list, name='resource-detail'),
]
