
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'), # SignUp page
    path('login/', views.login_view, name='login'),  # LogIn page
    path('logout/', views.logout_view, name='logout'), # LogOut page
]
