import form as form
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django import forms
from .models import Profile, FileModel, TestModel
from .forms import TestForm, FilesFormSet


def index(request):
    id = request.GET.get('id')
    obj = None
    error = ""
    files = None
    try:
        profile = Profile.objects.get(user=request.user)
    except (Profile.DoesNotExist, TypeError):
        profile = None
    if id and profile:
        obj = get_object_or_404(TestModel, id=id)  # , user=profile)
        files = FileModel.objects.filter(test=obj)
    else:
        files = FileModel.objects.none()
    fields = ["file"]
    widgets = {"file": forms.FileInput(attrs={"class": "form-control"})}
    files_formset = forms.modelformset_factory(FileModel, form=FilesFormSet, fields=fields, widgets=widgets, extra=0)
    if request.method == "POST":
        testForm = TestForm(request.POST, request.FILES)
        files_formset = files_formset(request.POST, request.FILES)
        if testForm.is_valid() and files_formset.is_valid():
            testResponse = testForm.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            testResponse.user = profile
            testResponse.save()
            for form in files_formset:
                fileResponse = form.save(commit=False)
                fileResponse.test = testResponse
                fileResponse.save()
            return render(request, f"testing/index.html/?{testResponse.id}", {"form": testForm, "files_formset": files_formset, "error": error})
    files_formset = files_formset(queryset=files)
    testForm = TestForm(instance=obj if id else None)
    for i in range(len(files_formset)):
        files_formset[i].fields["file"].label_suffix = ""
        files_formset[i].fields["file"].label = ""
        files_formset[i].path = f"/uploads/{files[i]}"
        files_formset[i].name = "/".join(str(files[i]).split("/")[1:])
    return render(request, "testing/index.html", {"form": testForm, "files_formset": files_formset, "error": error})
