# Generated by Django 2.0 on 2018-01-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human', '0007_auto_20180125_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='client',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='task',
        ),
        migrations.AddField(
            model_name='profile',
            name='point',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Reward',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]