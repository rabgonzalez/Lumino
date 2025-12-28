import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from factories import StudentFactory, SubjectFactory, TeacherFactory, UserFactory

# ==============================================================================
# URL Patterns
# ==============================================================================

TESTLANG = 'en'

ROOT_URL = f'/{TESTLANG}/'

LOGIN_URL = f'/{TESTLANG}/login/'
LOGOUT_URL = f'/{TESTLANG}/logout/'
SIGNUP_URL = f'/{TESTLANG}/signup/'

USER_DETAIL_URL = f'/{TESTLANG}/users/{{username}}/'
USER_EDIT_URL = f'/{TESTLANG}/user/edit/'
USER_LEAVE_URL = f'/{TESTLANG}/user/leave/'
SUBJECT_LIST_URL = f'/{TESTLANG}/subjects/'
SUBJECT_DETAIL_URL = f'/{TESTLANG}/subjects/{{subject_code}}/'
SUBJECT_ENROLL_URL = f'/{TESTLANG}/subjects/enroll/'
SUBJECT_UNENROLL_URL = f'/{TESTLANG}/subjects/unenroll/'
SUBJECT_GRADE_CERTIFICATE_URL = f'/{TESTLANG}/subjects/certificate/'
LESSON_DETAIL_URL = f'/{TESTLANG}/subjects/{{subject_code}}/lessons/{{lesson_pk}}/'
LESSON_ADD_URL = f'/{TESTLANG}/subjects/{{subject_code}}/lessons/add/'
LESSON_EDIT_URL = f'/{TESTLANG}/subjects/{{subject_code}}/lessons/{{lesson_pk}}/edit/'
LESSON_DELETE_URL = f'/{TESTLANG}/subjects/{{subject_code}}/lessons/{{lesson_pk}}/delete/'
MARKS_LIST_URL = f'/{TESTLANG}/subjects/{{subject_code}}/marks/'
MARKS_EDIT_URL = f'/{TESTLANG}/subjects/{{subject_code}}/marks/edit/'


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
