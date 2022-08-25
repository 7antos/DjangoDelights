import django_filters
from .models import Ingredient, Purchase, MenuItem
from django import forms


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains',
                                     widget=forms.TextInput(
                                         attrs={"class": "input-bar input-with-logo search-bar normal-input",
                                                "placeholder": "Ingredients Search"}))

    class Meta:
        model = Ingredient
        fields = ['name', ]


class MenuItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains',
                                     widget=forms.TextInput(
                                         attrs={"class": "input-bar input-with-logo search-bar normal-input",
                                                "placeholder": "Menu Search"}))

    class Meta:
        model = MenuItem
        fields = ['name', ]


class PurchaseFilter(django_filters.FilterSet):
    menuItem__name = django_filters.CharFilter(lookup_expr='contains',
                                               widget=forms.TextInput(
                                                   attrs={"class": "input-bar input-with-logo search-bar normal-input",
                                                          "placeholder": "Menu Search"}))

    class Meta:
        model = Purchase
        fields = ['menuItem__name', ]
