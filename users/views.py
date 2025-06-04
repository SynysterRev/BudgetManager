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

    def get_context_data(self, **kwargs):
        kwargs['profile_form'] = UpdateUserForm(instance=self.request.user)
        kwargs['password_form'] = PasswordChangeForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if 'profile' in request.POST:
            profile_form = UpdateUserForm(request.POST, instance=self.request.user)
            if profile_form.is_valid():
                user = profile_form.save()
                return JsonResponse({"success": True,
                                     "data": {"username": user.last_name,
                                              "email": user.email,
                                              "first_name": user.first_name}})
            else:
                return JsonResponse({
                    "success": False,
                    "errors": profile_form.errors},
                    status=400)
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_object(self, queryset=...):
        return self.request.user
