# Generated by Django 2.0 on 2018-02-24 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0004_auto_20180224_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='label',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='label',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]