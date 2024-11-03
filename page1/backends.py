from pyexpat.errors import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from requests import request
from .models import Person


User = get_user_model()

class GoogleAuthBackend(ModelBackend):
    print("Enter to backend")
    
    def authenticate(self, request, user=None):
        # Check if the user is already authenticated
        if user is not None:
            return user

        # Get user information from the request (e.g., from Google authentication)
        google_user_id = request.GET.get('google_user_id')
        email = request.GET.get('email')
        # Add more attributes as needed

        # Check if the user exists in the Person table
        try:
            person = Person.objects.get(user_id__username=google_user_id)
        except Person.DoesNotExist:
            # If the user does not exist, create a new Person record
            person = Person(
                user_id=User.objects.get(username=google_user_id),
                email=email,
                # Set other attributes
            )
            person.save()

        return person
