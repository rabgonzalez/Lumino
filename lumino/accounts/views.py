from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import UserSignupForm

FALLBACK_REDIRECT = 'index'

def user_login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', reverse(FALLBACK_REDIRECT)))
    
    if request.method == 'POST':
        if (form := AuthenticationForm(data=request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
            return redirect(request.GET.get('next', reverse(FALLBACK_REDIRECT)))
    else:
        form = AuthenticationForm()
    return render(request, 'auth_form.html', {'form': form, 'type':'login'})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse(FALLBACK_REDIRECT))

def user_signup(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', reverse(FALLBACK_REDIRECT)))
    
    if request.method == 'POST':
        if (form := UserSignupForm(request.POST)).is_valid():
            user = form.save()
            login(request, user)
            msg = _('Welcome to Lumino. Nice to see you!')
            messages.success(request, msg)
            return redirect(request.GET.get('next', reverse(FALLBACK_REDIRECT)))
    else:
        form = UserSignupForm()
    return render(request, 'auth_form.html', {'form': form, 'type':'signup'})
