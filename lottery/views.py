from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from lottery.models import Task, ProgressTask
from lottery.serializers import ProgressTaskSerializer, TaskSerializer

import logging
testlog = logging.getLogger('testdevelop')


class TaskView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user

        if 'label' in self.kwargs:
            label = self.kwargs['label']
            try:
                queryset = Task.objects.get_t(user, label)
            except Exception as error:
                testlog.warning(error)
                queryset = []
        else:
            queryset = Task.objects.get_t(user)

        return queryset

class ProgressTaskView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = ProgressTaskSerializer

    def get_queryset(self):
        user = self.request.user

        if 'label' in self.kwargs:
            label = self.kwargs['label']
            try:
                queryset = ProgressTask.objects.get_progress_task(user, label)
            except Exception as error:
                testlog.warning(error)
                queryset = []

        else:
            queryset = ProgressTask.objects.get_progress_task(user)

        return queryset


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def finish_task(request):
    if ('label' in request.data):
        try:
            finished_task = ProgressTask.objects.finish_task_by_label(
                request.user, request.data['label'])
            if finished_task:
                serializer = TaskSerializer(finished_task)
                return Response(serializer.data)
            else:
                return Response({"message": "Task already finished or closed"},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print (error)
            return Response({"message": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "parameter \'label\' not in scoope"},
                        status=status.HTTP_400_BAD_REQUEST)
