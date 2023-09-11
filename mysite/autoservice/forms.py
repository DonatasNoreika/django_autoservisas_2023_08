
from django import forms
from .models import UzsakymoKomentaras

class UzsakymoKomentarasForm(forms.ModelForm):
    class Meta:
        model = UzsakymoKomentaras
        fields = ["tekstas"]