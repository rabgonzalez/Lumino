import pytest
from pytest_django.asserts import assertRedirects

AUTH_URLS = [
    # SUBJECTS
    '/subjects/',
    '/subjects/AAA/',
    '/subjects/AAA/lessons/add/',
    '/subjects/AAA/lessons/1/',
    '/subjects/AAA/lessons/17/edit/',
    '/subjects/AAA/lessons/17/delete/',
    '/subjects/AAA/marks/',
    '/subjects/AAA/marks/edit/',
    '/subjects/enroll/',
    '/subjects/unenroll/',
    # USERS
    '/users/guido/',
    '/user/edit/',
    '/user/leave/',
]

testdata = [(url, f'/login/?next={url}') for url in AUTH_URLS]


@pytest.mark.parametrize('auth_url, redirect_url', testdata)
@pytest.mark.django_db
def test_login_required(client, auth_url, redirect_url):
    response = client.get(auth_url, follow=True)
    assertRedirects(response, redirect_url)
