from django.urls import path
from . import views

urlpatterns = [
    # Main AI server page
    path('', views.ai_server_view, name="ai-server"),
]
