# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def signup_view(request):
    """
    Handle user registration.

    Displays a registration form and processes the creation of a new user.
    On successful registration, logs in the user and redirects to the home page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Bind form data
        if form.is_valid():
            form.save()  # Create new user and save it to database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get(
                'password1')  # Get raw password
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, f"Account created successfully for {username}!")
            return redirect('home')  # Redirect to home page
    else:
        form = UserCreationForm()  # Instantiate an empty form

    # Render the signup page with the form
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    Displays a login form and authenticates the user. 
    Redirects to the home page on successful login, or reloads the login page with an error message on failure.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()  # Instantiate an empty form

    # Render the login page with the form
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.

    Logs out the currently authenticated user and redirects to the home page.
    """
    logout(request)
    return redirect('home')  # Redirect to home page
