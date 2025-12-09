import random
import re
from http import HTTPStatus

import pytest
from django.core.mail import EmailMessage
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from factories.subjects import EnrollmentFactory, LessonFactory, SubjectFactory
from subjects.models import Enrollment
from subjects.tasks import deliver_certificate
from tests import conftest

# ==============================================================================
# SUBJECT LIST
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_page_contains_expected_subjects_for_teacher_role(
    client, teacher, another_teacher
):
    own_teaching = SubjectFactory.create_batch(5, teacher=teacher)
    another_teaching = SubjectFactory.create_batch(5, teacher=another_teacher)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_LIST_URL)
    response_text = response.content.decode()
    for subject in own_teaching:
        assert re.search(rf'\b{subject.code}\b', response_text, re.S | re.M)
    for subject in another_teaching:
        assert not re.search(rf'\b{subject.code}\b', response_text, re.S | re.M)


@pytest.mark.dependency(
    depends=['test_subject_list_page_contains_expected_subjects_for_teacher_role']
)
@pytest.mark.django_db
def test_subject_list_page_contains_links_for_subject_details_for_teacher_role(client, teacher):
    teaching = SubjectFactory.create_batch(5, teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_LIST_URL)
    for subject in teaching:
        href = f'href="{conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code)}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_list_page_does_not_contain_enroll_link_for_teacher_role(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertNotContains(response, f'href="{conftest.SUBJECT_ENROLL_URL}"')


@pytest.mark.django_db
def test_subject_list_page_does_not_contain_unenroll_link_for_teacher_role(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertNotContains(response, f'href="{conftest.SUBJECT_UNENROLL_URL}"')


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_page_contains_expected_subjects_for_student_role(
    client, student, another_student
):
    own_enrollments = EnrollmentFactory.create_batch(5, student=student)
    another_enrollments = EnrollmentFactory.create_batch(5, student=another_student)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    response_text = response.content.decode()
    for enrollment in own_enrollments:
        assert re.search(rf'\b{enrollment.subject.code}\b', response_text, re.S | re.M)
    for enrollment in another_enrollments:
        assert not re.search(rf'\b{enrollment.subject.code}\b', response_text, re.S | re.M)


@pytest.mark.dependency(
    depends=['test_subject_list_page_contains_expected_subjects_for_student_role']
)
@pytest.mark.django_db
def test_subject_list_page_contains_expected_subject_links_for_student_role(client, student):
    enrollments = EnrollmentFactory.create_batch(5, student=student)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    for enrollment in enrollments:
        href = f'href="{conftest.SUBJECT_DETAIL_URL.format(subject_code=enrollment.subject.code)}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_list_page_contains_enroll_link_for_student_role(client, student):
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertContains(response, f'href="{conftest.SUBJECT_ENROLL_URL}"')


@pytest.mark.django_db
def test_subject_list_page_contains_unenroll_link_for_student_role(client, student):
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertContains(response, f'href="{conftest.SUBJECT_UNENROLL_URL}"')


@pytest.mark.django_db
def test_subject_list_page_contains_request_grade_certificate_link_when_all_subjects_have_mark_for_student_role(
    client, student
):
    EnrollmentFactory.create_batch(5, student=student, none_mark_probablity=0)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertContains(response, f'href="{conftest.SUBJECT_GRADE_CERTIFICATE_URL}"')


@pytest.mark.django_db
def test_subject_list_page_does_not_contain_request_grade_certificate_link_when_all_subjects_do_not_have_mark_for_student_role(
    client, student
):
    EnrollmentFactory.create_batch(5, mark=None, student=student)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_LIST_URL)
    assertNotContains(response, f'href="{conftest.SUBJECT_GRADE_CERTIFICATE_URL}"')


# ==============================================================================
# SUBJECT DETAIL
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_subject_detail_page_contains_expected_lessons_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    subject_lessons = LessonFactory.create_batch(5, subject=subject)
    another_lessons = LessonFactory.create_batch(5)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in subject_lessons:
        assertContains(response, lesson.title)
    for lesson in another_lessons:
        assertNotContains(response, lesson.title)


@pytest.mark.django_db
def test_subject_detail_page_contains_lesson_links_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lessons = LessonFactory.create_batch(5, subject=subject)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = conftest.LESSON_DETAIL_URL.format(
            subject_code=subject.code, lesson_pk=lesson.pk
        )
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_contains_edit_lesson_links_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lessons = LessonFactory.create_batch(5, subject=subject)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = conftest.LESSON_EDIT_URL.format(
            subject_code=subject.code, lesson_pk=lesson.pk
        )
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_contains_delete_lesson_links_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lessons = LessonFactory.create_batch(5, subject=subject)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = conftest.LESSON_DELETE_URL.format(
            subject_code=subject.code, lesson_pk=lesson.pk
        )
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_contains_add_lesson_link_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    href = f'href="{conftest.LESSON_ADD_URL.format(subject_code=subject.code)}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_contains_edit_marks_link_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    href = f'href="{conftest.MARKS_LIST_URL.format(subject_code=subject.code)}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_subject_detail_page_contains_expected_lessons_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    subject = enrollment.subject
    subject_lessons = LessonFactory.create_batch(5, subject=subject)
    another_lessons = LessonFactory.create_batch(5)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in subject_lessons:
        assertContains(response, lesson.title)
    for lesson in another_lessons:
        assertNotContains(response, lesson.title)


@pytest.mark.django_db
def test_subject_detail_page_contains_lesson_links_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    subject = enrollment.subject
    lessons = LessonFactory.create_batch(5, subject=subject)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = conftest.LESSON_DETAIL_URL.format(
            subject_code=subject.code, lesson_pk=lesson.pk
        )
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_does_not_contain_edit_lesson_link_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    subject = enrollment.subject
    lesson = LessonFactory(subject=subject)
    lesson_detail_url = conftest.LESSON_EDIT_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    href = f'href="{lesson_detail_url}"'
    assertNotContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_does_not_contain_delete_lesson_link_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    subject = enrollment.subject
    lesson = LessonFactory(subject=subject)
    lesson_detail_url = conftest.LESSON_DELETE_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    href = f'href="{lesson_detail_url}"'
    assertNotContains(response, href)


@pytest.mark.django_db
def test_subject_detail_page_shows_subject_mark_when_exists_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    enrollment.mark = 9
    enrollment.save()
    subject = enrollment.subject
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    response_text = response.content.decode()
    msg = rf'Your mark for this subject:.*?{enrollment.mark}'
    assert re.search(msg, response_text, re.S | re.M)


@pytest.mark.django_db
def test_subject_detail_is_forbidden_for_non_enrolled_students(client, student, subject):
    client.force_login(student)
    response = client.get(conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# ADD LESSON
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_add_lesson_page_displays_form_correctly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.LESSON_ADD_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '<form')
    assertContains(response, 'novalidate')
    assertContains(response, 'name="title"')
    assertContains(response, 'name="content"')


@pytest.mark.django_db
def test_add_lesson_works_properly(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    client.force_login(teacher)
    title, content = 'Django is awesome', 'Please learn Django!'
    payload = dict(title=title, content=content)
    response = client.post(
        conftest.LESSON_ADD_URL.format(subject_code=subject.code), payload, follow=True
    )
    assertContains(response, 'Lesson was successfully added.')
    assertRedirects(response, conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert subject.lessons.get(title=title, content=content) is not None


@pytest.mark.django_db
def test_add_lesson_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    client.force_login(teacher)
    response = client.get(conftest.LESSON_ADD_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_add_lesson_is_forbidden_for_students(client, student, subject):
    client.force_login(student)
    response = client.get(conftest.LESSON_ADD_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# LESSON DETAIL
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_lesson_detail_page_contains_expected_lesson_content_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_lesson_detail_page_contains_edit_lesson_link_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    lesson_detail_url = conftest.LESSON_DETAIL_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    lesson_edit_url = conftest.LESSON_EDIT_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    response = client.get(lesson_detail_url)
    href = f'href="{lesson_edit_url}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_lesson_detail_page_contains_delete_lesson_link_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    lesson_detail_url = conftest.LESSON_DETAIL_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    lesson_edit_url = conftest.LESSON_EDIT_URL.format(
        subject_code=subject.code, lesson_pk=lesson.pk
    )
    response = client.get(lesson_detail_url)
    href = f'href="{lesson_edit_url}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_lesson_detail_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_lesson_detail_page_contains_expected_lesson_content_for_student_role(client, student):
    enrollment = EnrollmentFactory(student=student)
    subject = enrollment.subject
    lesson = LessonFactory(subject=subject)
    client.force_login(student)
    response = client.get(
        conftest.LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_lesson_detail_is_forbidden_for_non_enrolled_students(client, student, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(student)
    response = client.get(
        conftest.LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# EDIT LESSON
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_edit_lesson_page_displays_form_correctly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_EDIT_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '<form')
    assertContains(response, 'novalidate')
    assertContains(response, 'name="title"')
    assertContains(response, 'name="content"')
    assertContains(response, lesson.title)
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_edit_lesson_works_properly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    title, content = 'Django is awesome', 'Please learn Django!'
    payload = dict(title=title, content=content)
    url = conftest.LESSON_EDIT_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.OK
    assert response.request['PATH_INFO'] == url
    assert (edited_lesson := subject.lessons.get(pk=lesson.pk)) is not None
    assert edited_lesson.title == title
    assert edited_lesson.content == content
    assertContains(response, 'Changes were successfully saved.')


@pytest.mark.django_db
def test_edit_lesson_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_EDIT_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_edit_lesson_is_forbidden_for_student_role(client, student, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(student)
    response = client.get(
        conftest.LESSON_EDIT_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# DELETE LESSON
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_delete_lesson_works_properly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_DELETE_URL.format(subject_code=subject.code, lesson_pk=lesson.pk),
        follow=True,
    )
    assertContains(response, 'Lesson was successfully deleted.')
    assertRedirects(response, conftest.SUBJECT_DETAIL_URL.format(subject_code=subject.code))
    assert subject.lessons.filter(pk=lesson.pk).count() == 0


@pytest.mark.django_db
def test_delete_lesson_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(teacher)
    response = client.get(
        conftest.LESSON_DELETE_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_delete_lesson_is_forbidden_for_student_role(client, student, subject):
    lesson = LessonFactory(subject=subject)
    client.force_login(student)
    response = client.get(
        conftest.LESSON_DELETE_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# MARK LIST
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_mark_list_page_contains_expected_content_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    enrollments = EnrollmentFactory.create_batch(5, subject=subject, none_mark_probablity=0)
    client.force_login(teacher)
    response = client.get(conftest.MARKS_LIST_URL.format(subject_code=subject.code))
    for enrollment in enrollments:
        student = enrollment.student
        assertContains(response, f'{student.first_name} {student.last_name}')
        assertContains(response, enrollment.mark)
        assertContains(response, conftest.USER_DETAIL_URL.format(username=student.username))


@pytest.mark.django_db
def test_mark_list_page_contains_link_to_edit_marks_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    client.force_login(teacher)
    response = client.get(conftest.MARKS_LIST_URL.format(subject_code=subject.code))
    href = f'href="{conftest.MARKS_EDIT_URL.format(subject_code=subject.code)}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_mark_list_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    client.force_login(teacher)
    response = client.get(conftest.MARKS_LIST_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_mark_list_is_forbidden_for_students(client, student, subject):
    client.force_login(student)
    response = client.get(conftest.MARKS_LIST_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# EDIT MARKS
# ==============================================================================


@pytest.mark.django_db
def test_edit_marks_page_displays_marks_properly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    enrollments = EnrollmentFactory.create_batch(5, subject=subject, none_mark_probablity=0)
    client.force_login(teacher)
    response = client.get(conftest.MARKS_EDIT_URL.format(subject_code=subject.code))
    response_text = response.content.decode()
    for enrollment in enrollments:
        assert re.search(rf'value="{enrollment.mark}"', response_text, re.I | re.M | re.S)


@pytest.mark.django_db
def test_edit_marks_works_properly_for_teacher_role(client, teacher):
    subject = SubjectFactory(teacher=teacher)
    enrollments = EnrollmentFactory.create_batch(5, subject=subject)
    num_enrollments = len(enrollments)
    client.force_login(teacher)
    payload = {
        'form-TOTAL_FORMS': num_enrollments,
        'form-INITIAL_FORMS': num_enrollments,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1000,
    }
    for enroll_idx, enrollment in enumerate(enrollments):
        payload[f'form-{enroll_idx}-id'] = enrollment.pk
        payload[f'form-{enroll_idx}-mark'] = random.randint(1, 10)
    url = conftest.MARKS_EDIT_URL.format(subject_code=subject.code)
    response = client.post(url, payload, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert response.request['PATH_INFO'] == url
    assertContains(response, 'Marks were successfully saved.')
    for enroll_idx in range(num_enrollments):
        enrollment_pk = payload[f'form-{enroll_idx}-id']
        mark = payload[f'form-{enroll_idx}-mark']
        assert Enrollment.objects.get(pk=enrollment_pk).mark == mark


@pytest.mark.django_db
def test_edit_is_forbidden_for_non_teaching_teachers(client, teacher, subject):
    client.force_login(teacher)
    response = client.get(conftest.MARKS_EDIT_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_edit_marks_is_forbidden_for_student_role(client, student, subject):
    client.force_login(student)
    response = client.get(conftest.MARKS_EDIT_URL.format(subject_code=subject.code))
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# ENROLL SUBJECTS
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_enroll_subjects_is_forbidden_for_teacher_role(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_ENROLL_URL)
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_enroll_subjects_page_displays_expected_subjects_for_student_role(client, student):
    subjects = SubjectFactory.create_batch(5)
    enrollments = EnrollmentFactory.create_batch(5, student=student)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_ENROLL_URL)
    response_text = response.content.decode()
    for unenrolled_subject in subjects:
        assert re.search(
            rf'<label.*?\b{unenrolled_subject.code}\b.*?</label>', response_text, re.M | re.S
        )
    for enrollment in enrollments:
        assert not re.search(
            rf'<label.*?\b{enrollment.subject.code}\b.*?</label>', response_text, re.M | re.S
        )


@pytest.mark.django_db
def test_enroll_subjects_works_properly_for_student_role(client, student):
    subjects = SubjectFactory.create_batch(5)
    subject_pks = [s.pk for s in subjects]
    client.force_login(student)
    payload = dict(subjects=subject_pks)
    response = client.post(conftest.SUBJECT_ENROLL_URL, payload, follow=True)
    assertContains(response, 'Successfully enrolled in the chosen subjects.')
    assertRedirects(response, conftest.SUBJECT_LIST_URL)
    enrolled_subject_pks = list(
        Enrollment.objects.filter(student=student).values_list('subject_id', flat=True)
    )
    assert enrolled_subject_pks == subject_pks


# ==============================================================================
# UNENROLL SUBJECTS
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_unenroll_subjects_is_forbidden_for_teacher_role(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_UNENROLL_URL)
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_unenroll_subjects_page_displays_expected_subjects_for_student_role(client, student):
    subjects = SubjectFactory.create_batch(5)
    enrollments = EnrollmentFactory.create_batch(5, student=student)
    client.force_login(student)
    response = client.get(conftest.SUBJECT_UNENROLL_URL)
    response_text = response.content.decode()
    for unenrolled_subject in subjects:
        assert not re.search(
            rf'<label.*?\b{unenrolled_subject.code}\b.*?</label>', response_text, re.M | re.S
        )
    for enrollment in enrollments:
        assert re.search(
            rf'<label.*?\b{enrollment.subject.code}\b.*?</label>', response_text, re.M | re.S
        )


@pytest.mark.django_db
def test_unenroll_subjects_works_properly_for_student_role(client, student):
    enrollments = EnrollmentFactory.create_batch(5, student=student)
    subject_pks = [e.subject.pk for e in enrollments]
    client.force_login(student)
    payload = dict(subjects=subject_pks)
    response = client.post(conftest.SUBJECT_UNENROLL_URL, payload, follow=True)
    assertContains(response, 'Successfully unenrolled from the chosen subjects.')
    assertRedirects(response, conftest.SUBJECT_LIST_URL)
    enrolled_subject_pks = Enrollment.objects.filter(student=student).values_list(
        'subject_id', flat=True
    )
    assert enrolled_subject_pks.count() == 0


# ==============================================================================
# REQUEST GRADE CERTIFICATE
# ==============================================================================

# ------------
# TEACHER ROLE
# ------------


@pytest.mark.django_db
def test_request_grade_certificate_is_forbidden_for_teacher_role(client, teacher):
    client.force_login(teacher)
    response = client.get(conftest.SUBJECT_UNENROLL_URL)
    assert response.status_code == HTTPStatus.FORBIDDEN


# ------------
# STUDENT ROLE
# ------------


@pytest.mark.django_db
def test_request_grade_certificate_works_properly_for_student_role(
    client, student, settings, monkeypatch
):
    sent_mail = False

    def mock_deliver_certificate(base_url, test_student):
        deliver_certificate(base_url, test_student)

    def mock_send_email(*args, **kwargs):
        nonlocal sent_mail
        sent_mail = True

    try:
        monkeypatch.setattr(deliver_certificate, 'delay', mock_deliver_certificate)
        monkeypatch.setattr(EmailMessage, 'send', mock_send_email)
        certificate = (
            settings.BASE_DIR / f'media/certificates/{student.username}_grade_certificate.pdf'
        )

        client.force_login(student)
        response = client.get('/subjects/certificate/')
        assert response.status_code == HTTPStatus.OK

        clean_response = re.sub(r'<.*?>', '', response.content.decode())
        clean_response = re.sub(r' {2,}', ' ', clean_response)
        msg = f'You will get the grade certificate quite soon at {student.email}'
        assert msg in clean_response, 'El mensaje de feedback no se ha dado correctamente'
        assert certificate.exists(), (
            'El certificado de calificaciones no se ha generado en la ruta esperada'
        )
        assert sent_mail, 'No se ha invocado al método send() de EmailMessage.'
    except Exception as err:
        raise err
    finally:
        certificate.unlink(missing_ok=True)


@pytest.mark.django_db
def test_request_grade_certificate_is_forbidden_when_any_subject_does_not_have_mark(
    client, student
):
    enrollments = EnrollmentFactory.create_batch(5, student=student)
    enrollments[0].mark = None
    enrollments[0].save()
    client.force_login(student)
    response = client.get('/subjects/certificate/')
    assert response.status_code == HTTPStatus.FORBIDDEN
