from django import forms

from django.contrib.auth import get_user_model

# HAY QUE HACER QUE SE COMPRUEBE SI ES ALUMNO CON UN MIDDLEWARE
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {'password' : forms.PasswordInput}
    
    def save(self, *args, **kwargs):
        # username = self.cleaned_data['username']
        # password = self.cleaned_data['password']
        # if user := authenticate(args, username=username, password=password):
        #     login(args, user)
        user = get_user_model().objects.first(self.cleaned_data['username'])
        return user

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        required = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {'password' : forms.PasswordInput}
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        return user
