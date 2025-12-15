from django.shortcuts import get_object_or_404
from .models import Subject

class SubjectConverter:
    regex = '[A-Z]{3}'

    def to_python(self, subject_code: str) -> Subject:
        return get_object_or_404(Subject, code=subject_code)
    
    def to_url(self, subject: Subject) -> str:
        return subject.code