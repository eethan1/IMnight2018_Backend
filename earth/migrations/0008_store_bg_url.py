# Generated by Django 2.0.3 on 2018-03-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0007_auto_20180310_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='bg_url',
            field=models.URLField(default='https://i.imgur.com/67A5cyq.jpg'),
        ),
    ]
