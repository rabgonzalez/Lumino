from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    code = models.CharField(unique=True)
    name = models.CharField()
    teacher = models.ForeignKey(get_user_model(), related_name='teaching', on_delete=models.PROTECT)
    students = models.ManyToManyField(
        get_user_model(), related_name='enrolled', through='subjects.Enrollment'
    )

    def __str__(self, *args, **kwargs):
        return f'{self.code}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', args={self})

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField()
    content = models.TextField(blank=True)

    def __str__(self, *args, **kwargs):
        return f'{self.title}'


class Enrollment(models.Model):
    student = models.ForeignKey(
        get_user_model(), related_name='enrollments', on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self, *args, **kwargs):
        return f'{self.student} | {self.subject} | {self.mark} |{self.enrolled_at}'
