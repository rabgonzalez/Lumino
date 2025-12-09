import pytest
from django.contrib import admin

from subjects.models import Enrollment, Lesson, Subject
from users.models import Profile


@pytest.mark.parametrize(
    'model',
    [Subject, Lesson, Enrollment, Profile],
)
@pytest.mark.django_db
def test_models_are_registered_in_admin(model):
    assert model in admin.site._registry, (
        f'El modelo "{model.__name__}" no está registrado en el admin'
    )
