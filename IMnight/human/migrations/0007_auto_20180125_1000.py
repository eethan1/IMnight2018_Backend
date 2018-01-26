# Generated by Django 2.0 on 2018-01-25 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('human', '0006_auto_20180120_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('rewarded', models.DateTimeField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('due_date', models.DateTimeField()),
                ('credit', models.PositiveIntegerField()),
                ('activated', models.BooleanField(default=False)),
                ('category', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='reward',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Task'),
        ),
    ]
