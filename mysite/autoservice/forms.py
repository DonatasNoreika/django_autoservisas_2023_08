from django import forms
from .models import UzsakymoKomentaras, Profile
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
