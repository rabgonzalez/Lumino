import pytest

from factories.subjects import SubjectRelatedFactory
from subjects.management.commands import get_subject_stats


@pytest.mark.django_db
def test_management_command_to_show_subject_stats(capsys):
    NUM_SUBJECTS = 5
    NUM_ENROLLMENTS_PER_SUBJECT = 10

    command = get_subject_stats.Command()
    test_data = []
    subjects = SubjectRelatedFactory.create_batch(
        NUM_SUBJECTS, enrollments__size=NUM_ENROLLMENTS_PER_SUBJECT
    )
    for subject in subjects:
        try:
            marks = (
                subject.enrollments.all().filter(mark__isnull=False).values_list('mark', flat=True)
            )
            avg_mark = sum(marks) / len(marks)
        except ZeroDivisionError:
            avg_mark = 0
        test_data.append({'subject': subject, 'avg_mark': avg_mark})
    command.handle()
    excected_output = '\n'.join(f'{d["subject"].code}: {d["avg_mark"]:.2f}' for d in test_data)
    captured = capsys.readouterr()
    assert captured.out.strip() == excected_output


@pytest.mark.django_db
def test_management_command_to_show_subject_stats_when_no_marks_exist(capsys):
    NUM_SUBJECTS = 3
    NUM_ENROLLMENTS_PER_SUBJECT = 5

    command = get_subject_stats.Command()
    subjects = SubjectRelatedFactory.create_batch(
        NUM_SUBJECTS, enrollments__size=NUM_ENROLLMENTS_PER_SUBJECT, enrollments__mark=None
    )
    command.handle()
    excected_output = '\n'.join(f'{subject.code}: 0.00' for subject in subjects)
    captured = capsys.readouterr()
    assert captured.out.strip() == excected_output
