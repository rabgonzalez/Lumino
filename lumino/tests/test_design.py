import re

import pytest

from subjects.models import Lesson, Subject
from tests import conftest


def test_template_inheritance(client):
    response = client.get(conftest.ROOT_URL)
    assert 'base.html' in [t.name for t in response.templates]


def test_template_includes(client):
    response = client.get(conftest.ROOT_URL)
    assert re.search('(includes/)?header.html', ''.join([t.name for t in response.templates]))


def test_template_contains_css_links(client):
    response = client.get(conftest.ROOT_URL)
    response_text = response.content.decode()
    assert re.search(r'<link[^>]+href="[^"]+bootstrap[^"]+\.css"', response_text, re.S | re.M)
    assert re.search(
        r'<link[^>]+href="[^"]+(main|custom|styles?)\.css"', response_text, re.S | re.M
    )


def test_message_middleware_is_enabled(settings):
    assert 'django.contrib.messages.middleware.MessageMiddleware' in settings.MIDDLEWARE


@pytest.mark.parametrize(
    'model',
    [Subject, Lesson],
)
@pytest.mark.django_db
def test_model_contains_get_absolute_url_method(model):
    assert hasattr(model, 'get_absolute_url')
    assert callable(getattr(model, 'get_absolute_url'))


def test_default_language_is_set_to_english(settings):
    assert settings.LANGUAGE_CODE == 'en-us'
