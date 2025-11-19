from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class TopUpForm(forms.Form):
    student_username = forms.CharField(label="Student Username")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class PaymentForm(forms.Form):
    team_username = forms.CharField(label="Team Username")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    description = forms.CharField(max_length=255, required=False)
