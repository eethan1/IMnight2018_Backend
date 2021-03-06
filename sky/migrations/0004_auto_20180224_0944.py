# Generated by Django 2.0 on 2018-02-24 09:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0003_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='label',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='course',
            name='label',
            field=models.SlugField(default=123921832973197927391929371923, unique=True),
            preserve_default=False,
        ),
    ]
