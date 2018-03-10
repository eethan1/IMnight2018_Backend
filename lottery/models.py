from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

import datetime
import random
import hashlib
import logging
testlog = logging.getLogger('testdevelop')

TASK_CATEGORY_CHOICE = (
    (1, "每日任務"),
    (2, "限時任務"),
    (3, "彩蛋"),
    (4, "閱讀文章")
)


def is_task(task_label):
    tasks = Task.objects.filter(label=task_label)

    if tasks:
        return True
    else:
        return False


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=500)
    due_date = models.DateTimeField(blank=False, null=False)
    credit = models.PositiveIntegerField(default=0, blank=False, null=False)
    activated = models.BooleanField(default=False)
    category = models.SmallIntegerField(
        default=1, choices=TASK_CATEGORY_CHOICE)
    label = models.SlugField(unique=True, blank=True)

    objects = models.manager

    def __str__(self):
        return "%s %s have %d credit, due in %s, label:%s" % (self.name, TASK_CATEGORY_CHOICE[self.category - 1][1], self.credit, self.due_date, self.label)

    def save(self, *args, **kwargs):
        hashkey = self.name + str(self.due_date)
        task_label = hash(hashkey) % (10 ** 20)
        task_label = slugify(task_label)
        try:
            self.label = task_label
        except Exception as error:
            testlog.error(error)
            task_label = hash(hashkey**2) % (10 ** 20)
            task_label = slugify(task_label)
            self.label = task_label

        super(Task, self).save(*args, **kwargs)


class ProgressTaskManager(models.Manager):
    def get_progress_task(self, user, task_label=None):
        if task_label is not None:
            tasks = Task.objects.filter(label=task_label)
            if tasks is not None:
                return ProgressTask.objects.filter(user=user).filter(task__in=tasks)
            else:
                raise Exception(
                    "this task label dosen't exist,  label=%s", task_label)
        else:
            return ProgressTask.objects.filter(user=user)

    def finish_task_by_label(self, user, task_label):
        task = Task.objects.filter(label=task_label).first()
        if task:
            try:
                obj, created = ProgressTask.objects.get_or_create(
                    user=user, task=task)
                print(obj, created)
            except Exception as error:
                testlog.error(error)

            if created:
                user.profile.add_point(task.credit)
                return True
            else:
                if obj.last_active_date.date() != datetime.datetime.today().date():
                    user.profile.add_point(task.credit)
                    obj.last_active_date = datetime.datetime.today()
                    obj.save()
                    return True
                else:
                    return False
        else:
            return False


class ProgressTask(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE)
    last_active_date = models.DateTimeField(default=timezone.now)
    # is_finish = models.BooleanField(default=False)

    objects = ProgressTaskManager()

    def __str__(self):
        return "'%s' have a '%s' task created on %s." % (self.user.username, self.task.name, self.last_active_date)

    def save(self, *args, **kwargs):
        # Some identity check for the ProgressTask
        if timezone.now() > self.task.due_date:
            raise Exception("this task have been closed.")
        # create unique label used for chatroom
        super(ProgressTask, self).save(*args, **kwargs)
