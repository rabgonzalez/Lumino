from django.shortcuts import get_object_or_404
from .models import Subject, Lesson

class SubjectConverter:
    regex = '[A-Z]{3}'

    def to_python(self, subject_code: str) -> Subject:
        return get_object_or_404(Subject, code=subject_code)
    
    def to_url(self, subject: Subject) -> str:
        return subject.code
    
class LessonConverter:
    regex = '[0-9]+'

    def to_python(self, lesson_pk: int) -> Lesson:
        return get_object_or_404(Lesson, code=lesson_pk)
    
    def to_url(self, lesson: Lesson) -> int:
        return lesson.pk