# Generated by Django 2.0 on 2018-01-24 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0004_auto_20180123_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='holdingvocher',
            name='be_used',
            field=models.BooleanField(default=False),
        ),
    ]