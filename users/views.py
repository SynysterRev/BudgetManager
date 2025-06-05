from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from users.forms import SignupForm, UpdateUserForm, PasswordChangeForm
from users.models import User


class SignupView(SuccessMessageMixin, CreateView):
    template_name = "users/signup.html"
    success_url = reverse_lazy("login")
    form_class = SignupForm
    success_message = "Your account was created successfully!"


class SettingsView(LoginRequiredMixin, View):
    model = User
    template_name = "users/settings.html"
    success_message = "Password changed successfully"

    def get_context_data(self, **kwargs):
        kwargs['profile_form'] = UpdateUserForm(instance=self.request.user)
        kwargs['password_form'] = PasswordChangeForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if 'profile' in request.POST:
            profile_form = UpdateUserForm(request.POST, instance=user)
            if profile_form.is_valid():
                user = profile_form.save()
                return JsonResponse({"success": True,
                                     "data": {"lastName": user.last_name,
                                              "email": user.email,
                                              "firstName": user.first_name}},
                                    status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "errors": profile_form.errors},
                    status=400)

        if 'password' in request.POST:
            password_form = PasswordChangeForm(request.POST, user=user)
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get("new_password")
                user.set_password(new_password)
                user.save()
                # Updating the password logs out all other sessions for the user
                # except the current one.
                update_session_auth_hash(self.request, self.request.user)
                return JsonResponse({
                    "success": True,
                    "successMessage": self.success_message
                }, status=200
                )
            else:
                return JsonResponse({
                    "success": False,
                    "errors": password_form.errors},
                    status=400
                )

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_object(self, queryset=...):
        return self.request.user
