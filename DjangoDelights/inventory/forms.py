from django import forms
from django.core.exceptions import ValidationError

from .models import *


class IngredientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-bar normal-input', 'placeholder': 'Enter Ingredient Name'}), required=True)
    price = forms.DecimalField(required=True, initial=0, min_value=0.01, decimal_places=2,
                               max_digits=6, widget=forms.NumberInput(
                                attrs={'class': "input-bar input-with-logo dollar-bar small-input",
                                                "placeholder": "Price"}))

    class Meta:
        model = Ingredient
        fields = ("name", "price")


class MenuItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-bar normal-input', 'placeholder': 'Enter Ingredient Name'}), required=True)
    price = forms.DecimalField(required=True, min_value=0.01, decimal_places=2,
                               max_digits=6, widget=forms.NumberInput(
                                attrs={'class': "input-bar input-with-logo dollar-bar small-input",
                                                "placeholder": "Price"}))
    minStock = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(
                                    attrs={'class': "input-bar small-without-logo-input",
                                           "placeholder": "Min Stock"}))

    class Meta:
        model = MenuItem
        fields = ("name", "price", "minStock")

    def clean_name(self):
        data = self.cleaned_data['name']
        if MenuItem.objects.filter(name=data, deleted=False):
            raise ValidationError('Menu already exists')
        return data
