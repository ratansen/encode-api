# Generated by Django 3.2.11 on 2022-01-09 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20220109_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='password',
        ),
    ]
