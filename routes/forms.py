from django import forms
from .models import *
from cities.models import City


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={"class": 'form-control'}))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control'}))
    trouth_cities = forms.ModelMultipleChoiceField(label='Через следующие города',
                                                   queryset=City.objects.all(), required=False,
                                                   widget=forms.SelectMultiple(attrs={"class": 'form-control'}))
    traveling_time = forms.IntegerField(label='Желаемое время в пути', required=True,
                                        widget=forms.NumberInput(attrs={"class": 'form-control'}))
                

class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', required=True,
                           widget=forms.TextInput(attrs={"class": 'form-control'}))
    from_city = forms.CharField(label='Откуда',  widget=forms.HiddenInput(attrs={"class": 'form-control'}))
    to_city = forms.CharField(label='Куда',  widget=forms.HiddenInput(attrs={"class": 'form-control'}))
    routes = forms.CharField(label='Маршрут',  widget=forms.Textarea(attrs={"class": 'form-control'}))
    travel_time = forms.IntegerField(label='Время в пути',
                                     widget=forms.HiddenInput(attrs={"class": 'form-control'}))
    trouth_cities = forms.CharField(widget=forms.HiddenInput(attrs={"class": 'form-control'}))
    
    class Meta(object):
        model = Route
        fields = ('name', 'from_city', 'to_city', 'trouth_cities', 'travel_time')
