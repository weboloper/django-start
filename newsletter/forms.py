from django import forms
from .models import Subscriber
from django.contrib import messages


class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Email",
    }), label="")

    class Meta:
        model = Subscriber
        fields = ('email', )

