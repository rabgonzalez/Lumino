from django import forms
from .models import Subject, Enrollment, Lesson

class LessonsForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

class EnrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['subjects'].queryset = Subject.objects.exclude(students=student)

class UnenrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['subjects'].queryset = student.enrolled.all()

class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']