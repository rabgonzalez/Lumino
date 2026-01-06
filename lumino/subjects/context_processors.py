from users.models import Profile 

def subjects(request) -> dict:
    try:
        if request.user.profile.role == Profile.Role.STUDENT:
            return dict(subjects=request.user.enrolled.all())
        elif request.user.profile.role ==  Profile.Role.TEACHER:
            return dict(subjects=request.user.teaching.all())
    except AttributeError:
        pass
    return {}
