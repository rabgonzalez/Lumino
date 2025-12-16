from django.shortcuts import redirect, render
from .models import Subject
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .forms import UnenrollSubjectForm

STUDENT = 'S'
TEACHER = 'T'
FALLBACK_REDIRECT = 'index'

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
            return HttpResponseForbidden("You don't have access")
    elif request.user.profile.role == TEACHER:
        if not request.user.enrollments.filter(subject=subject):
            return HttpResponseForbidden("You don't have access")


    mark = request.user.enrollments.filter(subject=subject).get().mark
    return render(request, 'subject_detail.html', dict(subject=subject, mark=mark))

@login_required
def unenroll_subjects(request):
    if request.method == 'POST':
        if(form := UnenrollSubjectForm(request.POST, user=request.user)).is_valid():
            subjects_to_remove = form.cleaned_data['subjects']
            for subject in subjects_to_remove:
                request.user.enrolled.remove(subject.id)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = UnenrollSubjectForm(user=request.user)
    return render(request, 'enrollment_form.html', dict(form=form))
