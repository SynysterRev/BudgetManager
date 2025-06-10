from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView

from expenses.models import Transaction, Category
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
    password_success_message = "Password changed successfully"
    profile_success_message = "Profile updated successfully"

    def get_context_data(self, **kwargs):
        context = kwargs or {}
        context.update({
            'profile_form': UpdateUserForm(instance=self.request.user),
            'password_form': PasswordChangeForm(user=self.request.user),
            'total_transactions': Transaction.objects.filter(
                user=self.request.user).count(),
            'total_categories': Category.objects.filter(user=self.request.user).count(),
            'creation_date': self.request.user.date_joined.strftime("%d/%m/%Y"),
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if 'profile' in request.POST:
            profile_form = UpdateUserForm(request.POST, instance=user)
            if profile_form.is_valid():
                user = profile_form.save()
                return JsonResponse({"success": True,
                                     "data": {"lastName": user.last_name,
                                              "email": user.email,
                                              "firstName": user.first_name},
                                     "successMessage": self.profile_success_message},
                                    status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "errors": profile_form.errors},
                    status=400)

        if 'password' in request.POST:
            password_form = PasswordChangeForm(data=request.POST, user=user)
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get("new_password")
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(self.request, self.request.user)
                return JsonResponse({
                    "success": True,
                    "successMessage": self.password_success_message
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


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('login')

    def get_object(self, queryset=...):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)
