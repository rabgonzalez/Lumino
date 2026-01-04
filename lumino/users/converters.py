from django.shortcuts import get_object_or_404
from .models import Profile

class ProfileConverter:
    regex = '\w+'

    def to_python(self, profile_username: str) -> Profile:
        return get_object_or_404(Profile, user__username=profile_username)
    
    def to_url(self, profile: Profile) -> str:
        return profile.user.username