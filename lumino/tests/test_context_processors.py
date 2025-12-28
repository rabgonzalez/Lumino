import pytest

from factories import EnrollmentFactory, SubjectFactory
from tests import conftest


@pytest.mark.django_db
def test_subjects_are_available_for_teachers_in_all_templates_through_context_processor(
    client, teacher
):
    subjects = SubjectFactory.create_batch(10, teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.USER_DETAIL_URL.format(username=teacher.username))
    assert list(response.context['subjects']) == subjects


@pytest.mark.django_db
def test_subjects_are_available_for_students_in_all_templates_through_context_processor(
    client, student
):
    enrollments = EnrollmentFactory.create_batch(10, student=student)
    client.force_login(student)
    response = client.get(conftest.USER_DETAIL_URL.format(username=student.username))
    assert list(response.context['subjects']) == [e.subject for e in enrollments]
