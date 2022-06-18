from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Profile, FileModel, TestModel, PunishmentModel
from .forms import TestForm


def index(request):
    id = request.GET.get('id')
    obj = None
    files = None
    punishments = None
    try:
        profile = Profile.objects.get(user=request.user)
    except (Profile.DoesNotExist, TypeError):
        profile = None
    if id and profile:
        obj = get_object_or_404(TestModel, id=id)  # , user=profile)
        files = FileModel.objects.filter(test=obj)
        punishments = PunishmentModel.objects.filter(test=obj)
    else:
        files = FileModel.objects.none()
        punishments = PunishmentModel.objects.none()
    fields_files = ["file"]
    widgets_files = {"file": forms.FileInput(attrs={"class": "form-control"})}
    files_formset = forms.modelformset_factory(FileModel, fields=fields_files, widgets=widgets_files, extra=0)
    fields_punishment = ["profile", "punishment"]
    widgets_punishment = {
        "profile": forms.Select(attrs={"class": "form-control", "required": False}),
        "punishment": forms.Select(attrs={"class": "form-control", "required": False})
    }
    punishment_formset = forms.modelformset_factory(PunishmentModel, fields=fields_punishment, widgets=widgets_punishment, extra=0)
    if request.method == "POST":
        testForm = TestForm(request.POST, request.FILES, instance=obj if id else None)
        files_formset = files_formset(request.POST, request.FILES, prefix="file")
        punishment_formset = punishment_formset(request.POST, prefix="punishment")
        if testForm.is_valid():
            testResponse = testForm.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            testResponse.user = profile
            testResponse.save()
            for form in files_formset:
                if form.hidden_fields()[0].value() and int(form.hidden_fields()[0].value()) < 0:
                    form_id = int(form.hidden_fields()[0].value()) * -1
                    form = get_object_or_404(FileModel, id=form_id, test=obj)
                    form.delete()
                    continue
                fileResponse = form.save(commit=False)
                fileResponse.test = testResponse
                fileResponse.save()
            for form in punishment_formset:
                if form.hidden_fields()[0].value() and int(form.hidden_fields()[0].value()) < 0:
                    form_id = int(form.hidden_fields()[0].value()) * -1
                    form = get_object_or_404(PunishmentModel, id=form_id, test=obj)
                    form.delete()
                    continue
                punishmentResponse = form.save(commit=False)
                punishmentResponse.test = testResponse
                punishmentResponse.save()
            return redirect(f"/?id={testResponse.id}")
        else:
            print(testForm.errors)
            print(files_formset.errors)
    files_formset = files_formset(queryset=files, prefix="file")
    punishment_formset = punishment_formset(queryset=punishments, prefix="punishment")
    testForm = TestForm(instance=obj if id else None)
    # print(dir(testForm.fields["elimination_plan"]))

    # testForm.fields["elimination_plan"].label_suffix = ": "
    for i in range(len(files_formset)):
        files_formset[i].fields["file"].label_suffix = ""
        files_formset[i].fields["file"].label = ""
        files_formset[i].path = f"/uploads/{files[i]}"
        files_formset[i].name = "/".join(str(files[i]).split("/")[1:])
    return render(request, "testing/index.html", {"form": testForm, "files_formset": files_formset, "punishment_formset": punishment_formset})


# def edit_form(request, id, **kwargs):
#     obj = get_object_or_404(TestModel, id=id)
#     # files = FileModel.objects.filter(test=obj)
#     testForm = TestForm(instance=obj)

