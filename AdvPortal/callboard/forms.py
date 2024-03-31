from allauth.account.forms import SignupForm
from string import hexdigits
import random
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Advert, CATEGORY


class CommonSignupForm(SignupForm):

    def save(self, request):
        # Ensure you call the parent class's save. Save() returns a User object.
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=_('Activation code'),           # Код активации
            message=_('Account activation code'),    # Код активации аккаунта
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user


class AdvertForm(forms.ModelForm):
#    title = forms.CharField(max_length=30, widget=forms.TextInput(required=True))
    category = forms.CharField(
        max_length=20, empty_value='Категория не выбрана',
        widget=forms.Select(choices=CATEGORY)
    )

    class Meta:
        model = Advert
        fields = ['user', 'title', 'content', 'category', 'price', 'contacts']
        label = [_('User'), _('Title'), _('Content'), _('Category'), _('Price'), _('Contacts')]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'contacts': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if content == title:
            raise ValidationError(
                'Текст не должен совпадать с заголовком.'
            )

        return cleaned_data
