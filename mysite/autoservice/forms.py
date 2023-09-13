from django import forms
from .models import UzsakymoKomentaras, Profile, Uzsakymas
from django.contrib.auth.models import User


class UzsakymoKomentarasForm(forms.ModelForm):
    class Meta:
        model = UzsakymoKomentaras
        fields = ["tekstas"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

class UzsakymasForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['automobilis', 'deadline', 'status']
        widgets = {"deadline": DateTimeInput()}