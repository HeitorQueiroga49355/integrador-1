from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Try to find user by username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        # Check password
        if user.check_password(password):
            return user
        return None
