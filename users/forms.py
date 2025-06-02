from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from users.models import User
from widgets.widgets import InputWidget


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email"]
        widgets = {
            "email": InputWidget(
                attrs={
                    "title": "Email",
                    "placeholder": "Enter your email",
                    "type": "email",
                }
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = InputWidget(
            attrs={
                "title": "Password",
                "type": "password",
                "placeholder": "Create your password",
            }
        )
        self.fields["password2"].widget = InputWidget(
            attrs={
                "title": "Confirm password",
                "type": "password",
                "placeholder": "Confirm your password",
            }
        )


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=InputWidget(
            attrs={"title": "Email", "placeholder": "Enter your email", "type":
                "email", "autocomplete": "email", "name": "email", }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=InputWidget(
            attrs={
                "title": "Password",
                "placeholder": "Enter your password",
                "type": "password",
                "autocomplete": "current-password",
            }
        ),
    )


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "email", ]
        widgets = {
            "email": InputWidget(
                attrs={
                    "title": "Email Address", "disabled": True,
                }
            ),
            "last_name": InputWidget(
                attrs={
                    "title": "Last Name", "disabled": True,
                }
            ),
            "first_name": InputWidget(
                attrs={
                    "title": "First Name", "disabled": True,
                }
            ),
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_password = forms.CharField()
