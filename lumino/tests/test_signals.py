import pytest


@pytest.mark.django_db
def test_profile_is_created_after_user_saved(django_user_model):
    user = django_user_model.objects.create_user(username='guido', password='1234')
    assert user.profile is not None
