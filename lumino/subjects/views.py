from django.shortcuts import render
from .models import Subject
from django.contrib.auth.decorators import login_required

@login_required
def subject_list(request):
    modules = {}
    if request.user.profile.role == 'S':
        modules = student_subject_list(request)
    elif request.user.profile.role == 'T':
        modules = teacher_subject_list(request)
    return render(request, 'subjects.html', dict(modules=modules))

def student_subject_list(request):
    return request.user.enrollments.all()


def teacher_subject_list(request):
    return request.user.teaching.all()