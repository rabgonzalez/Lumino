from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from users.models import Profile

from .forms import EditMarkForm, EnrollSubjectsForm, LessonsForm, UnenrollSubjectsForm
from .models import Enrollment, Lesson, Subject
from .tasks import deliver_certificate

FALLBACK_REDIRECT = 'index'
FORBIDDEN_MESSAGE = _("You don't have access")


def user_not_in_module(request, subject: Subject):
    if request.user.profile.role == Profile.Role.STUDENT:
        print(request.user.enrollments.filter(subject=subject))
        if not request.user.enrollments.filter(subject=subject) == '<QuerySet []>':
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

    elif request.user.profile.role == Profile.Role.TEACHER:
        print(subject.teacher)
        print(request.user)
        print(subject.teacher != request.user)
        if subject.teacher != request.user:
            print('ta mal')
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)


@login_required
def subject_list(request):
    if request.user.profile.role == Profile.Role.STUDENT:
        return student_subject_list(request)
    elif request.user.profile.role == Profile.Role.TEACHER:
        return render(request, 'subjects.html')


@login_required
def student_subject_list(request):
    modules_with_mark = request.user.enrollments.filter(mark__isnull=False).count()
    if modules_with_mark == request.user.enrollments.count() and modules_with_mark > 0:
        certificate = True
    else:
        certificate = False
    return render(request, 'subjects.html', dict(certificate=certificate))


@login_required
def subject_detail(request, subject: Subject):
    user_not_in_module(request, subject)
    if request.user.profile.role == Profile.Role.STUDENT:
        mark = request.user.enrollments.filter(subject=subject).get().mark
    elif request.user.profile.role == Profile.Role.TEACHER:
        mark = None
    return render(request, 'subject_detail.html', dict(subject=subject, mark=mark))


@login_required
def add_lesson(request, subject: Subject):
    if request.user.profile.role != Profile.Role.TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if (form := LessonsForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            msg = _('Lesson was successfully added')
            messages.success(request, msg)
            return redirect('subjects:subject-list')
    form = LessonsForm()
    return render(request, 'form.html', dict(form=form))


@login_required
def lesson_detail(request, subject: Subject, lesson: Lesson):
    user_not_in_module(request, subject)
    return render(request, 'lesson_detail.html', dict(subject=subject, lesson=lesson))


@login_required
def edit_lesson(request, subject: Subject, lesson: Lesson):
    if request.user.profile.role != Profile.Role.TEACHER:
        raise PermissionDenied
    user_not_in_module(request, subject)
    if request.method == 'POST':
        if (form := LessonsForm(request.POST, instance=lesson)).is_valid():
            form.save()
            msg = _('Changes were successfully saved')
            messages.success(request, msg)
    form = LessonsForm(instance=lesson)
    return render(request, 'form.html', dict(form=form))


@login_required
def delete_lesson(request, subject: Subject, lesson: Lesson):
    if request.user.profile.role != Profile.Role.TEACHER:
        raise PermissionDenied
    user_not_in_module(request, subject)
    lesson.delete()
    msg = _('Lesson was successfully deleted')
    messages.success(request, msg)
    return redirect(subject)


@login_required
def mark_list(request, subject: Subject):
    if request.user.profile.role != Profile.Role.TEACHER:
        raise PermissionDenied
    user_not_in_module(request, subject)
    modules = subject.enrollments.all()
    return render(request, 'mark_list.html', dict(modules=modules, subject=subject))


@login_required
def edit_marks(request, subject: Subject):
    if request.user.profile.role != Profile.Role.TEACHER:
        raise PermissionDenied
    user_not_in_module(request, subject)
    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
    formset = MarkFormSet(queryset=queryset)
    return render(request, 'form.html', dict(form=formset, subject=subject))


@login_required
def enroll_subjects(request):
    if request.user.profile.role == Profile.Role.TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if (form := EnrollSubjectsForm(request.POST, student=request.user)).is_valid():
            subjects_to_enroll = form.cleaned_data['subjects']
            request.user.enrolled.add(*subjects_to_enroll)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = EnrollSubjectsForm(student=request.user)
    return render(request, 'form.html', dict(form=form))


@login_required
def unenroll_subjects(request):
    if request.user.profile.role == Profile.Role.TEACHER:
        raise PermissionDenied
    if request.method == 'POST':
        if (form := UnenrollSubjectsForm(request.POST, student=request.user)).is_valid():
            subjects_to_remove = form.cleaned_data['subjects']
            request.user.enrolled.remove(*subjects_to_remove)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = UnenrollSubjectsForm(student=request.user)
    return render(request, 'form.html', dict(form=form))


@login_required
def request_certificate(request):
    if request.user.profile.role == Profile.Role.TEACHER:
        raise PermissionDenied
    if request.user.enrollments.filter(mark__isnull=True).count() > 0:
        raise PermissionDenied
    deliver_certificate.delay(request.build_absolute_uri(), request.user)
    return render(request, 'deliver_certificate.html')
