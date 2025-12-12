import pytest
from pytest_django.asserts import assertRedirects

from tests import conftest

AUTH_URLS = [
    # SUBJECTS
    f'/{conftest.TESTLANG}/subjects/',
    f'/{conftest.TESTLANG}/subjects/AAA/',
    f'/{conftest.TESTLANG}/subjects/AAA/lessons/add/',
    f'/{conftest.TESTLANG}/subjects/AAA/lessons/1/',
    f'/{conftest.TESTLANG}/subjects/AAA/lessons/17/edit/',
    f'/{conftest.TESTLANG}/subjects/AAA/lessons/17/delete/',
    f'/{conftest.TESTLANG}/subjects/AAA/marks/',
    f'/{conftest.TESTLANG}/subjects/AAA/marks/edit/',
    f'/{conftest.TESTLANG}/subjects/enroll/',
    f'/{conftest.TESTLANG}/subjects/unenroll/',
    # USERS
    f'/{conftest.TESTLANG}/users/guido/',
    f'/{conftest.TESTLANG}/user/edit/',
    f'/{conftest.TESTLANG}/user/leave/',
]

testdata = [(url, f'{conftest.LOGIN_URL}?next={url}') for url in AUTH_URLS]


@pytest.mark.parametrize('auth_url, redirect_url', testdata)
@pytest.mark.django_db
def test_login_required(client, auth_url, redirect_url):
    response = client.get(auth_url, follow=True)
    assertRedirects(response, redirect_url)
