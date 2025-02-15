"""
URL configuration for emblab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path("users/", include('users.urls')),  # User authentication
    path("", include('home.urls')),  # Home page
    path("ai/", include('aiserver.urls')),  # AI server
    path("inventory/", include('inventory.urls')),  # Inventory
    # Booking Tables and Loaning Inventory
    path("book-loan/", include('bookloan.urls')),
    # Resources (e.g. books, tutorials, videos, etc.)
    path('resources/', include('resources.urls')),
]
