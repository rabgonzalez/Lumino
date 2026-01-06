from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import ProfileForm
from .models import Profile


@login_required
def user_detail(request, user: Profile):
    return render(request, 'user_profile.html', dict(profile=user))


@login_required
def edit_profile(request,):
    profile = request.user.profile
    if request.method == 'POST':
        if (form := ProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            form.save()
            msg = _('User profile has been successfully saved.')
            messages.success(request, msg)
            return redirect(profile)
    form = ProfileForm(instance=profile)
    return render(request, 'form.html', dict(form=form))


@login_required
def leave(request):
    if request.user.profile.role == Profile.Role.TEACHER:
        raise PermissionDenied
    request.user.delete()
    msg = _('Good bye! Hope to see you soon.')
    messages.success(request, msg)
    return redirect('index')
