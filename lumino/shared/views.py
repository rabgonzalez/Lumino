from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation

def index(request):
    if request.user.username:
        return redirect('subjects:subject-list')
    
    else:
        return render(request, 'index.html')

def setlang(request, langcode: str):
    next = request.GET.get('next', '/')
    translation.activate(langcode)
    response = redirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langcode)
    return response 