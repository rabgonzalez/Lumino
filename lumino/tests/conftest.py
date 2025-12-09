import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from factories.auth import UserFactory
from factories.subjects import SubjectFactory
from factories.users import StudentFactory, TeacherFactory

# ==============================================================================
# URL Patterns
# ==============================================================================

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
SIGNUP_URL = '/signup/'

USER_DETAIL_URL = '/users/{username}/'
USER_EDIT_URL = '/user/edit/'
USER_LEAVE_URL = '/user/leave/'

SUBJECT_LIST_URL = '/subjects/'
SUBJECT_DETAIL_URL = '/subjects/{subject_code}/'
SUBJECT_ENROLL_URL = '/subjects/enroll/'
SUBJECT_UNENROLL_URL = '/subjects/unenroll/'
SUBJECT_GRADE_CERTIFICATE_URL = '/subjects/certificate/'

LESSON_DETAIL_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/'
LESSON_ADD_URL = '/subjects/{subject_code}/lessons/add/'
LESSON_EDIT_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/edit/'
LESSON_DELETE_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/delete/'

MARKS_LIST_URL = '/subjects/{subject_code}/marks/'
MARKS_EDIT_URL = '/subjects/{subject_code}/marks/edit/'


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture(autouse=True)
def media_tmpdir(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / 'media'


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def another_student():
    return StudentFactory()


@pytest.fixture
def teacher():
    return TeacherFactory()


@pytest.fixture
def another_teacher():
    return TeacherFactory()


@pytest.fixture
def subject():
    return SubjectFactory()


@pytest.fixture
def image():
    img = Image.new('RGBA', size=(200, 200), color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return SimpleUploadedFile(
        name='test_image.png',
        content=buffer.getvalue(),
        content_type='image/png',
    )
