# Generated by Django 2.0 on 2018-01-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
