from django.contrib.auth.models import User

from rest_framework import serializers

from human.serializers import UserDetailsSerializer
from lottery.models import ProgressTask, Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class ProgressTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(required=True, many=True)
    user = UserDetailsSerializer(required=True, many=True)

    class Meta:
        model = ProgressTask
        fields = ('user', 'task', 'last_active_date',)
