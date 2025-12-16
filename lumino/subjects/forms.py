from django import forms
from .models import Subject

class UnenrollSubjectForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(), 
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UnenrollSubjectForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['subjects'].queryset = user.enrolled.all()