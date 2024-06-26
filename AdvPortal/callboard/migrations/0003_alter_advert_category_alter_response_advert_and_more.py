# Generated by Django 5.0.3 on 2024-03-25 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0002_category_alter_user_code_advert_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='adverts', to='callboard.category', verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='response',
            name='advert',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='callboard.advert', verbose_name='Advert'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL, verbose_name='Author of the ad'),
            preserve_default=False,
        ),
    ]
