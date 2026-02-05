# file: `pesquisador/mixins.py`
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from user.models import Profile
from user.utils import get_default_page_alias_by_user


class ResearcherRequiredMixin:
    def get(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and hasattr(user, 'profile') and user.profile.role == Profile.Role.RESEARCHER):
            return redirect(get_default_page_alias_by_user(request.user))
        return super().get(request, *args, **kwargs)