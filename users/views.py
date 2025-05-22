from django.urls import reverse_lazy
from users.forms import SignupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView


class SignupView(SuccessMessageMixin, CreateView):
    template_name = "users/signup.html"
    success_url = reverse_lazy("login")
    form_class = SignupForm
    success_message = "Your account was created successfully!"
