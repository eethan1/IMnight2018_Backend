from django.contrib.auth.models import User

from rest_framework import serializers

from human.serializers import UserDetailsSerializer
from lottery.models import ProgressTask, Task


class SingleTaskSerializer(serializers.ModelSerializer):
    """
    with all fields, to access many task should use Tasks to prevent label field exposed
    """
    class Meta:
        model = Task
        fields = '__all__'

class TasksSerializer(serializers.ModelSerializer):
    """
    without label field
    """
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'due_date', 'credit', 'activated', 'category')


class ProgressTaskSerializer(serializers.ModelSerializer):
    task = SingleTaskSerializer(required=True)
    user = UserDetailsSerializer(required=True)

    class Meta:
        model = ProgressTask
        fields = ('user', 'task', 'last_active_date',)
