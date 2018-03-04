from django import forms
from .models import *


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Название', required=True, widget=forms.TextInput(attrs={"class": 'form-control'}))
    
    class Meta(object):
        model = City
        fields = ('name',)
