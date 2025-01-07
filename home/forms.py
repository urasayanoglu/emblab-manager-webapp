from django import forms
from .models import UserFeedback


class FeedbackForm(forms.ModelForm):
    """
    A form for submitting user feedback.

    Dynamically adjusts the requirements of the `name` and `email` fields
    based on the authentication status of the user.
    """
    class Meta:
        model = UserFeedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'message': 'Your Feedback',
        }

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to dynamically set field requirements based on user authentication.

        Args:
            user (User): The currently authenticated user, passed through kwargs.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If the user is not logged in, mark name and email as required
        if not user or not user.is_authenticated:
            self.fields['name'].required = True
            self.fields['email'].required = True
