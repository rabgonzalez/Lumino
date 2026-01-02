from django.shortcuts import redirect, render
from .models import Subject, Lesson
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .forms import UnenrollSubjectsForm, EnrollSubjectsForm, LessonsForm
from django.contrib import messages
from django.utils.translation import gettext as _

STUDENT = 'S'
TEACHER = 'T'
FALLBACK_REDIRECT = 'index'
FORBIDDEN_MESSAGE = _("You don't have access")

def user_not_in_module(request, subject: Subject):
    if request.user.profile.role == STUDENT:
        if not request.user.enrollments.filter(subject=subject):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
        
    elif request.user.profile.role == TEACHER:
        if subject.teacher != request.user:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)    

@login_required
def subject_list(request):
    if request.user.profile.role == STUDENT:
        return student_subject_list(request)
    elif request.user.profile.role == TEACHER:
        return render(request, 'subjects.html')

@login_required
def student_subject_list(request):
    modules_with_mark = request.user.enrollments.filter(mark__isnull = False).count()
    if modules_with_mark == request.user.enrollments.count():
        certificate = True
    else:
        certificate = False
    return render(request, 'subjects.html', dict(certificate=certificate))    

@login_required
def subject_detail(request, subject: Subject):
    user_not_in_module(request, subject)
    if request.user.profile.role == STUDENT:
        mark = request.user.enrollments.filter(subject=subject).get().mark
    elif request.user.profile.role == TEACHER:
        mark = None
    return render(request, 'subject_detail.html', dict(subject=subject, mark=mark))

@login_required
def add_lesson(request, subject: Subject):
    if request.user.profile.role != TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if(form := LessonsForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            messages.success(request, 'Lesson was successfully added')
            return redirect('subjects:subject-list')
    form = LessonsForm()
    return render(request, 'enrollment_form.html', dict(form=form))

@login_required
def lesson_detail(request, subject: Subject, lesson: Lesson):
    user_not_in_module(request, subject)
    return render(request, 'lesson_detail.html', dict(subject=subject, lesson=lesson))

@login_required
def edit_lesson(request, subject: Subject, lesson: Lesson):
    if request.user.profile.role != TEACHER:
        raise PermissionDenied
    pass

@login_required
def delete_lesson(request, subject: Subject, lesson: Lesson):
    if request.user.profile.role != TEACHER:
        raise PermissionDenied
    pass

@login_required
def mark_list(request, subject: Subject):
    if request.user.profile.role != TEACHER:
        raise PermissionDenied
    pass

@login_required
def edit_marks(request, subject: Subject):
    if request.user.profile.role != TEACHER:
        raise PermissionDenied
    pass

@login_required
def enroll_subjects(request):
    if request.user.profile.role == TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if(form := EnrollSubjectsForm(request.POST, student=request.user)).is_valid():
            subjects_to_enroll = form.cleaned_data['subjects']
            request.user.enrolled.add(*subjects_to_enroll)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = EnrollSubjectsForm(student=request.user)
    return render(request, 'enrollment_form.html', dict(form=form))

@login_required
def unenroll_subjects(request):
    if request.user.profile.role == TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if(form := UnenrollSubjectsForm(request.POST, student=request.user)).is_valid():
            subjects_to_remove = form.cleaned_data['subjects']
            request.user.enrolled.remove(*subjects_to_remove)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = UnenrollSubjectsForm(student=request.user)
    return render(request, 'enrollment_form.html', dict(form=form))

@login_required
def request_certificate(request):
    if request.user.profile.role == TEACHER:
        raise PermissionDenied
    pass