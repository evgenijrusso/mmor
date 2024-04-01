from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

CATEGORY = [
    ('tanks', _('Tanks')), ('healers', _('Healers')), ('dd', _('DD')), ('merchants', _('Merchants')),
    ('guildmasters', _('Guildmasters')), ('questgivers', _('Questgivers')), ('blacksmiths', _('Blacksmiths')),
    ('tanners', _('Tanners')), ('alchemists', _('Alchemists')), ('spell_masters', _('Spell Masters'))
]


class User(AbstractUser):
    """ Пользователь """
    code = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Code'))  # доп. поле для user


class Advert(models.Model):
    """ Объявление """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='Author of the ad', related_name='adverts',
    )
    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY)
    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Description'))  # Описание
    price = models.DecimalField(_('Price'), null=True, blank=True, max_digits=7, decimal_places=1)
    contacts = models.TextField(_('Contacts'))  # Контакты
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created data')
    file = models.FileField("File", upload_to="files/", blank=True, null=True)

    def __str__(self):
        return f'{self.title}, {self.category}, {self.created}'

    def get_absolute_url(self):  # 'pk' как в url.py, иначе не работает
        return reverse('advert_detail', kwargs={'pk': self.pk})  # как вариант f'/adverts/{self.id}'

    class Meta:
        verbose_name = _('Advert')
        verbose_name_plural = _('Advert')
        ordering = ['-created']


class Response(models.Model):
    text = models.TextField(_('Reply text'))  # Текст ответа
    response_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of response'))  # Дата ответа
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        verbose_name=_('Advert'),
        related_name='responses'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author of the ad',
        related_name='responses'
    )
    accept = models.BooleanField(default=False, verbose_name='Accept')  # принимать пользователем объевления

    def __str__(self):
        return f'{self.text[:30]}...'

    def get_absolute_url(self):
        return reverse('response_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
        ordering = ['-response_date']
