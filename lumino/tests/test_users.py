import re
from http import HTTPStatus
from pathlib import Path

import pytest
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from tests import conftest
from users.models import Profile

# ==============================================================================
# USER DETAIL
# ==============================================================================


@pytest.mark.dependency()
@pytest.mark.django_db
def test_user_detail_page_handles_login_required(client, user):
    url = conftest.USER_DETAIL_URL.format(username=user.username)
    response = client.get(url, follow=True)
    assertRedirects(response, conftest.get_next_url(url))


@pytest.mark.django_db
def test_user_detail_displays_all_elements(client, student, teacher):
    client.force_login(student)
    response = client.get(conftest.USER_DETAIL_URL.format(username=student.username))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, f'{student.first_name} {student.last_name}')
    assertContains(response, 'Student')
    assertContains(response, student.email)
    assertContains(response, student.profile.bio)
    response_text = response.content.decode()
    # sorl-thumbnail creates this path for thumbnails
    assert re.search(r'<img.*?src="/media/cache.*?"', response_text, re.S | re.M)

    response = client.get(conftest.USER_DETAIL_URL.format(username=teacher.username))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, 'Teacher')


@pytest.mark.django_db
def test_user_detail_contains_link_to_edit_profile(client, user):
    client.force_login(user)
    response = client.get(conftest.USER_DETAIL_URL.format(username=user.username))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '/user/edit/')


@pytest.mark.django_db
def test_user_detail_as_student_contains_link_to_leave(client, student):
    client.force_login(student)
    response = client.get(conftest.USER_DETAIL_URL.format(username=student.username))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '/user/leave/')


@pytest.mark.django_db
def test_user_detail_as_teacher_does_not_contain_link_to_leave(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.USER_DETAIL_URL.format(username=teacher.username))
    assert response.status_code == HTTPStatus.OK
    assertNotContains(response, '/user/leave/')


@pytest.mark.django_db
def test_user_detail_non_existent_user_returns_404(client, user):
    client.force_login(user)
    response = client.get(conftest.USER_DETAIL_URL.format(username='non_existent_user'))
    assert response.status_code == HTTPStatus.NOT_FOUND


# ==============================================================================
# EDIT PROFILE
# ==============================================================================


@pytest.mark.dependency()
@pytest.mark.django_db
def test_edit_profile_page_handles_login_required(client):
    url = conftest.USER_EDIT_URL
    response = client.get(url, follow=True)
    assertRedirects(response, conftest.get_next_url(url))


@pytest.mark.django_db
def test_edit_profile_contains_right_user_info(client, user):
    client.force_login(user)
    response = client.get(conftest.USER_EDIT_URL)
    assertContains(response, user.profile.bio)
    # Find at least <input type="file">
    response_text = response.content.decode()
    assert re.search(r'<input.*?type="file"', response_text, re.S | re.M)
    # assertContains(response, user.profile.avatar.url)


@pytest.mark.django_db
def test_edit_profile_works_properly(client, user, image):
    try:
        client.force_login(user)
        payload = dict(bio='Python creator', avatar=image)
        response = client.post(conftest.USER_EDIT_URL, payload, follow=True)
        assertRedirects(response, conftest.USER_DETAIL_URL.format(username=user.username))
        profile = Profile.objects.get(user=user)
        assert profile.bio == payload['bio']
        assert profile.avatar.size == image.size, 'Error al guardar la imagen de avatar.'
        assertContains(response, 'User profile has been successfully saved.')
    except Exception as err:
        raise err
    finally:
        Path(profile.avatar.path).unlink(missing_ok=True)


# ==============================================================================
# LEAVE USER
# ==============================================================================


@pytest.mark.dependency()
@pytest.mark.django_db
def test_user_leaves_platform_page_handles_login_required(client):
    url = conftest.USER_LEAVE_URL
    response = client.get(url, follow=True)
    assertRedirects(response, conftest.get_next_url(url))


@pytest.mark.django_db
def test_user_leaves_platform_works(client, student, django_user_model):
    student_pk = student.pk
    client.force_login(student)
    response = client.get(conftest.USER_LEAVE_URL, follow=True)
    assertRedirects(response, conftest.ROOT_URL)
    User = django_user_model
    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=student_pk)
    assertContains(response, 'Good bye! Hope to see you soon.')


@pytest.mark.django_db
def test_user_leaves_platform_is_forbidden_for_teachers(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.USER_LEAVE_URL)
    assert response.status_code == HTTPStatus.FORBIDDEN
