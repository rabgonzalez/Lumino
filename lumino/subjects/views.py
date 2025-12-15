from django.shortcuts import render
from .models import Subject
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

STUDENT = 'S'
TEACHER = 'T'

@login_required
def subject_list(request):
    if request.user.profile.role == STUDENT:
        return student_subject_list(request)
    elif request.user.profile.role == TEACHER:
        return teacher_subject_list(request)

@login_required
def student_subject_list(request):
    modules = request.user.enrollments.all()
    modules_with_mark = request.user.enrollments.filter(mark__isnull = False).count()
    if modules_with_mark == request.user.enrollments.count():
        certificate = True
    else:
        certificate = False
    return render(request, 'subjects.html', dict(modules=modules, certificate=certificate))

@login_required
def teacher_subject_list(request):
    subjects = request.user.teaching.all()
    return render(request, 'subjects.html', dict(subjects=subjects))

@login_required
def subject_detail(request, subject: Subject):
    if request.user.profile.role == STUDENT:
        if not request.user.enrollments.filter(subject=subject):
            return HttpResponseForbidden("You don't have acces")
    elif request.user.profile.role == TEACHER:
        if not request.user.enrollments.filter(subject=subject):
            return HttpResponseForbidden("You don't have acces")


    mark = request.user.enrollments.filter(subject=subject).get().mark
    return render(request, 'subject_detail.html', dict(subject=subject, mark=mark))