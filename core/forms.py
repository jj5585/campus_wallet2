from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  # 👈 this was missing

from .models import Wallet

User = get_user_model()


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "class_name")
        help_texts = {field: "" for field in fields}  # remove default help texts

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove password help_texts
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        # placeholders + shared CSS class for nicer UI
        field_placeholders = {
            "username": "Choose a username",
            "email": "Your email address",
            "class_name": "Your class / section",
            "password1": "Password",
            "password2": "Confirm password",
        }

        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_classes + " auth-input").strip()

            if name in field_placeholders:
                field.widget.attrs["placeholder"] = field_placeholders[name]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_staff = False
        user.is_superuser = False
        if hasattr(user, "role"):
            user.role = "CUSTOMER"

        if commit:
            user.save()
            Wallet.objects.create(user=user, balance=0)

        return user


class TopUpForm(forms.Form):
    student_username = forms.CharField(label="Student Username")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class PaymentForm(forms.Form):
    team_username = forms.CharField(label="Team Username")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    description = forms.CharField(max_length=255, required=False)
