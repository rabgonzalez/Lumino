import pytest
from pytest_django.asserts import assertContains, assertRedirects

from tests import conftest


@pytest.mark.django_db
def test_index_page_shows_expected_content_when_user_is_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 200
    assertContains(response, 'Join Lumino. The cool education platform!')
    assertContains(response, conftest.LOGIN_URL)
    assertContains(response, conftest.SIGNUP_URL)


@pytest.mark.django_db
def test_index_page_behaves_as_expected_when_user_is_logged_in(client, user):
    client.force_login(user)
    response = client.get('/')
    assertRedirects(response, conftest.SUBJECT_LIST_URL)


@pytest.mark.django_db
def test_i18n_works_as_expected(client, teacher):
    client.force_login(teacher)
    response = client.get('/setlang/en/?next=/subjects/', follow=True)
    assertContains(response, 'My subjects')
    response = client.get('/setlang/es/?next=/subjects/', follow=True)
    assertContains(response, 'Mis módulos')
