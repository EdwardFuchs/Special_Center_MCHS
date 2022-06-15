from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from testing.models import Profile


class NewUserForm(UserCreationForm):
    last_name = forms.CharField(required=True, label="Фамилия")
    first_name = forms.CharField(required=True, label="Имя")
    middleName = forms.CharField(required=True, label="Отчество")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "first_name", "middleName")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, middleName=self.cleaned_data["middleName"])
            profile.save()
        return user



