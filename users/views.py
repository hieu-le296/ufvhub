from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    UserChangePasswordForm,
)
from django.contrib.auth import update_session_auth_hash
import json
from django.http import JsonResponse
from .serializer import UserSerailizer


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Your account {username} has been created!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


# LOGIN_URL in setting
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid:
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get("username")
            messages.success(request, f"Your account {username} has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserChangePasswordForm(request.user)

    context = {"form": form}
    return render(request, "users/password.html", context)


@login_required
def userSettings(request):
    user = request.user
    setting = user.profile

    seralizer = UserSerailizer(setting, many=False)

    return JsonResponse(seralizer.data, safe=False)


@login_required
def updateTheme(request):
    data = json.loads(request.body)
    theme = data["theme"]

    user = request.user
    user.profile.value = theme
    user.profile.save()
    print("Request:", theme)
    return JsonResponse("Updated..", safe=False)
