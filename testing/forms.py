from django.forms import ModelForm
from .models import TestModel, Profile, FileModel
from django.contrib.auth.models import User
from django import forms


class TestForm(ModelForm):
    class Meta:
        model = TestModel
        fields = ["user", "name", "text", "elimination_plan", "score"]
        widgets = {
            "user": forms.HiddenInput(),  # forms.TextInput(attrs={"class": "form-control", "readonly": True}),
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "text": forms.Textarea(attrs={"class": "form-control", "required": True, "rows": 3}),
            # "files": forms.ClearableFileInput(attrs={"class": "form-control", "multiple": True}),
            "elimination_plan": forms.FileInput(attrs={"class": "form-control"}),
            # "users": forms.Select(attrs={"class": "form-control", "multiple": True}),
            # "punishment": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "score": forms.Select(attrs={"class": "form-control", "required": True})
        }
        labels = {
            "name": "Название проверки",
            "text": "Основные недостатки",
            "score": "Оценка",
            "elimination_plan": "План устранения недостатков",
            # "users": "Привлечённые сотрудники",
            # "files": "Дополнительные файлы",
            "punishment": "Наказание",
        }


class FilesFormSet(FileModel):
    def __init__(self, *args, **kwargs):
        super(FileModel, self).__init__(*args, **kwargs)
        self.queryset = FileModel.objects.none()
        self.label_suffix = ""
# username = "TestUser"
# password = "TestUser"*2
# middleName = "Витальевич"
# user = User.objects.create_user(username=username, password=password)
# user.first_name = "Игорь"
# user.last_name = "Дынж"
# user.save()
# profile = Profile(user=user, middleName=middleName)
# profile.save()
#
# username = "TestUser1"
# password = "TestUser1"*2
# middleName = "Витальевич1"
# user = User.objects.create_user(username=username, password=password)
# user.first_name = "Игорь1"
# user.last_name = "Дынж1"
# user.save()
# profile = Profile(user=user, middleName=middleName)
# profile.save()
#
# user = User.objects.create_user(username="edward", password="pass")
# user.is_superuser = True
# user.is_staff = True
# user.save()
