# Generated by Django 2.0 on 2018-02-15 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human', '0008_auto_20180125_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.URLField(default='https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/10712978_745859095491727_8519447814807561759_n.jpg?oh=51a1b3c040bebb38f221053aeb2c42db&oe=5B16C07D'),
        ),
    ]
