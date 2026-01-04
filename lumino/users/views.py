from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def user_detail(request, user: Profile):
    return render(request, 'user_profile.html', dict(profile=user))