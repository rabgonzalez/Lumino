from django import forms
from .models import Subject, Enrollment
from django.shortcuts import render
from django.forms import modelformset_factory

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

    def edit_marks(request, subject: Subject):
        MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
        queryset = subject.enrollments.all()
        if request.method == 'POST':
            if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
                print(formset)
        else:
            formset = MarkFormSet(queryset=queryset)
        return render(request, 'subjects/marks/edit_marks.html', dict(subject=subject, formset=formset))