# Generated by Django 3.2 on 2023-06-21 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thirdpartyapp',
            name='description',
        ),
        migrations.RemoveField(
            model_name='thirdpartyapp',
            name='icon_url',
        ),
        migrations.RemoveField(
            model_name='thirdpartyapp',
            name='status',
        ),
    ]
