from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from testing.models import Profile


def register_request(request):
    error = ""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # profile = Profile.objects.get(user=request.user)
        # form = NewUserForm(request.POST, instance=profile)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Регистрация пройдена")
            return redirect("/")
        error = "Проверьте правильность информации"
        # messages.error(request, error)
    form = NewUserForm()

    return render(request=request, template_name="testing/register.html",
                  context={"register_form": form, "error": error})


def login_request(request):
    error = ""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # messages.info(request, f"Вы вошли как {username}.")
                return redirect("/")
            else:
                error = "Неправильное имя пользователя или пароль."
                # messages.error(request, error)
        else:
            error = "Неправильное имя пользователя или пароль."
            # messages.error(request, error)
    form = AuthenticationForm()
    return render(request=request, template_name="testing/login.html", context={"login_form": form, "error": error})


def logout_request(request):
    logout(request)
    return redirect("/")
