# Generated by Django 2.0.3 on 2018-03-18 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0008_store_bg_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]