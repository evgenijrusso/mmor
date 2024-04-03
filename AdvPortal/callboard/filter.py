from django import forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import User, Advert


class AdvertFilter(FilterSet):
    title = CharFilter(
        label='Содержит',
        lookup_expr='icontains'
    )

    user = ModelChoiceFilter(
        queryset=User.objects.all(),
        lookup_expr='exact',
        label='Пользователь',
        empty_label='Все авторы',
    )
    created = DateFilter(
        label='Опубликованы после',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form'})
    )

    class Meta:
        model = Advert
        fields = []

