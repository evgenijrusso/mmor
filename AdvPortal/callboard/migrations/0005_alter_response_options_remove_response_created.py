# Generated by Django 5.0.3 on 2024-04-01 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0004_alter_advert_category_advert_file_delete_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='response',
            options={'ordering': ['-response_date'], 'verbose_name': 'Response', 'verbose_name_plural': 'Responses'},
        ),
        migrations.RemoveField(
            model_name='response',
            name='created',
        ),
    ]
