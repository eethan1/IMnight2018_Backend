import datetime
import hashlib
import logging
import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

log = logging.getLogger('syslogger')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job = models.TextField(max_length=500, blank=True)
    job_description = models.TextField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    point = models.PositiveIntegerField(default=0, blank=False, null=False)
    img = models.URLField(
        default="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Default_profile_picture_%28male%29_on_Facebook.jpg/600px-Default_profile_picture_%28male%29_on_Facebook.jpg")
    isReadTutorial = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def add_point(self, reward):
        self.point += reward
        self.save()
        return self.point


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def is_client(user):
    username = user.username
    user_instance = User.objects.filter(username=username).filter(
        groups__name__exact="Clients")
    if user_instance:
        return True
    else:
        return False


def is_performer(user):
    username = user.username
    user_instance = User.objects.filter(username=username).filter(
        groups__name__exact="Performers")
    if user_instance:
        return True
    else:
        return False


class RelationshipManager(models.Manager):
    def get_performers(self, user):
        if is_performer(user):
            raise ValidationError(
                "You can't get performers list from a performer")

        performers = Relationship.objects.filter(client=user)
        return performers

    def get_clients(self, user):
        if is_client(user):
            raise ValidationError("You can't get clients list from a client")

        clients = Relationship.objects.filter(performer=user)
        return clients

    def is_performer_drawn(self, user):
        try:
            # 篩選使用者今天所建立的relationship
            # 有可能是自己抽的（user會在client欄位）
            # 有可能是被抽的（user會在performer欄位）
            daily_relationship = Relationship.objects.filter(
                Q(client=user) | Q(performer=user)).filter(
                created__date=datetime.date.today())
        except Exception as error:
            log.error("query今天建立的relationship的時候發生錯誤: %s" % error)
            return (False, None)

        if len(daily_relationship) > 0:
            # 今天有relationship建立

            if len(daily_relationship) > 2:
                log.error("%s 今天有超過2個relationship被建立" % user.username)

            for relationship in daily_relationship:
                if relationship.client == user:
                    # 使用者今天已經抽過卡
                    return (True, relationship)

        # 使用者今天還沒抽過卡
        return (False, None)

    def is_all_drawn(self, user):
        # 今天還沒有抽過資管人
        # own_performer_pk 是已經擁有關係的資管人名單
        own_performer_pk = [user.pk]
        own_relationship = Relationship.objects.filter(client=user)
        for relationship in own_relationship:
            own_performer_pk.append(relationship.performer.pk)
        own_relationship = Relationship.objects.filter(performer=user)
        for relationship in own_relationship:
            own_performer_pk.append(relationship.client.pk)

        try:
            # available_performers 是還可以抽的資管人名單
            available_performers = User.objects.filter(
                groups__name__exact="Performers").exclude(pk__in=own_performer_pk)
        except Exception as error:
            log.error("query還可以抽的資管人名單的時候發生錯誤: %s" % error)
            return (True, None)

        # 隨機抽資管人
        num = len(available_performers)
        if num <= 0:
            # 所有的資管人都已經抽完
            # 或是別的資管人都抽到你（在user也是資管人的情況下）
            return (True, None)
        else:
            return (False, available_performers)

    def get_daily(self, user):
        (is_performer_drawn, relationship) = self.is_performer_drawn(user)

        if is_performer_drawn:
            # 今天已經抽過資管人
            return [relationship]

        else:
            (is_all_drawn, available_performers) = self.is_all_drawn(user)

            if is_all_drawn:
                # 已經抽完全部資管人
                # 或是被抽完（當user是資管人）
                return Relationship.objects.none()
            else:
                # 隨機抽資管人
                num = len(available_performers)
                index = random.randint(0, num - 1)
                performer = available_performers[index]

                try:
                    daily_performer = self.create(
                        client=user, performer=performer)
                    daily_performer.save()
                    # 抽卡預設加30點
                    user.profile.add_point(30)
                except Exception as error:
                    log.error("建立新的relationship的時候發生錯誤: %s" % error)
                    return Relationship.objects.none()

                # return objects must be iterable
                return [daily_performer]

    def check_daily(self, user):
        # 檢查今天是否抽過資管人
        (is_performer_drawn, relationship) = self.is_performer_drawn(user)
        # 檢查是否已經抽完全部的資管人
        (is_all_drawn, available_performers) = self.is_all_drawn(user)

        return (is_performer_drawn, is_all_drawn)


class Relationship(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client')
    performer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='performer')
    created = models.DateTimeField(default=timezone.now)
    # this label is used to identify chatroom
    label = models.SlugField(unique=True, blank=True)

    # set the model manager to FriendshipManager()
    objects = RelationshipManager()

    class Meta:
        unique_together = ('client', 'performer')
        ordering = ['client', 'performer', '-created']

    def __str__(self):
        return "Client \"%s\" Performer \"%s\"" % (self.client.username, self.performer.username)

    def save(self, *args, **kwargs):
        if self.client == self.performer:
            log.error("嘗試建立performer == client 的 Relationship( %s )" %
                      self.client)

        # create unique label used for chatroom
        hashkey = self.client.username + \
            self.performer.username + str(self.created)
        relationship_label = hash(hashkey) % (10 ** 20)
        relationship_label = slugify(relationship_label)
        try:
            self.label = relationship_label
        except Exception as error:
            log.error(error)
            relationship_label = hash(hashkey**2) % (10 ** 20)
            relationship_label = slugify(relationship_label)
            self.label = relationship_label

        super(Relationship, self).save(*args, **kwargs)
