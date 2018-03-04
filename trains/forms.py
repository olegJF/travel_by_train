from django import forms
from .models import *
from cities.models import City


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Название', required=True, widget=forms.TextInput(attrs={"class": 'form-control'}))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={"class": 'form-control'}))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control'}))
    travel_time = forms.IntegerField(label='Время в пути', required=True,
                                     widget=forms.NumberInput(attrs={"class": 'form-control'}))
    
    class Meta(object):
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')
