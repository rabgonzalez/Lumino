STUDENT = 'S'
TEACHER = 'T'

def subjects(request) -> dict:
    try:
        if request.user.profile.role == STUDENT:
            return dict(modules=request.user.enrollments.all())
        elif request.user.profile.role == TEACHER:
            return dict(subjects=request.user.teaching.all())
    except AttributeError:
        pass
    return {}
