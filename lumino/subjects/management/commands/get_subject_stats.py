from django.core.management.base import BaseCommand
from subjects.models import Subject, Enrollment
from django.db.models import Avg

EMPTY_MARK = 0.00

class Command(BaseCommand):
    help = 'Show the average grade for each module.'

    def handle(self, *args, **kwargs):
        for subject in Subject.objects.all():
            if (enrollments := Enrollment.objects.filter(subject=subject).exclude(mark__isnull=True)):
                avg_mark = enrollments.aggregate(avg_mark=Avg('mark'))['avg_mark']
                self.stdout.write(f'{subject.code}: {avg_mark:.2f}')
            else:
                self.stdout.write(f'{subject.code}: {EMPTY_MARK:.2f}')
                