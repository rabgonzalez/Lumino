from django.shortcuts import render
from .models import Subject

def subject_list(request):
    subjects = {}
    return render(request, 'subjects.html', dict(subjects=subjects))