# Generated by Django 2.0 on 2018-01-20 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human', '0005_auto_20180118_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationship',
            options={'verbose_name': 'Relationship', 'verbose_name_plural': 'My Relationships'},
        ),
        migrations.AddField(
            model_name='message',
            name='readed',
            field=models.BooleanField(default=False),
        ),
    ]
