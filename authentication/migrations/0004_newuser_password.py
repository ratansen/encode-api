# Generated by Django 3.2.11 on 2022-01-09 06:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_newuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
