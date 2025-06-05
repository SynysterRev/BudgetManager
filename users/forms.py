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
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        label=_("current_password"),
        strip=False,
        widget=InputWidget(
            attrs={
                "title": "Current Password",
                "placeholder": "Enter your current password",
                "type": "password",
                "autocomplete": "current-password",
            }
        )
    )
    new_password = forms.CharField(
        label=_("new_password"),
        strip=False,
        widget=InputWidget(
            attrs={
                "title": "New Password",
                "placeholder": "Enter your new password",
                "type": "password",
            }
        ),
    )
    confirm_password = forms.CharField(
        label=_("confirm_password"),
        strip=False,
        widget=InputWidget(
            attrs={
                "title": "Confirm Password",
                "placeholder": "Confirm your password",
                "type": "password",
            }
        ),
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Your current password is incorrect")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password",
                           "Please make sure both password fields match.")
