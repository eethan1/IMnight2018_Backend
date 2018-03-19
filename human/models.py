from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import Group
from django.db.models import Q


import datetime
import random
import hashlib
import logging
testlog = logging.getLogger('testdevelop')


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

    def get_daily(self, user):
        # if is_performer(user):
        #     raise ValidationError(
        #         "You can't get daily_performer from a performer")

        try:
            daily_performer = Relationship.objects.filter(
                Q(client=user) | Q(performer=user)).filter(created__date=datetime.date.today()).first()
        except Exception as error:
            testlog.error(error)
            return Relationship.objects.none()

        if daily_performer:
            if daily_performer.client == user:
                # already draw daily performer
                print("draw")
                return [daily_performer]
        else:
            # not yet draw daily performer
            own_performer_pk = [user.pk]
            own_relationship = Relationship.objects.filter(client=user)
            for relationship in own_relationship:
                own_performer_pk.append(relationship.performer.pk)
            own_relationship = Relationship.objects.filter(performer=user)
            for relationship in own_relationship:
                own_performer_pk.append(relationship.client.pk)

            try:
                all_performers = User.objects.filter(
                    groups__name__exact="Performers").exclude(pk__in=own_performer_pk)
            except Exception as error:
                testlog.error(error)
                all_performers = []

            """random choice a performer and return"""
            num = len(all_performers)
            # check if already draw all performers
            if num <= 0:
                # all performer are draw
                return Relationship.objects.none()

            else:
                index = random.randint(0, num - 1)
                performer = all_performers[index]

                try:
                    daily_performer = self.create(
                        client=user, performer=performer)
                    daily_performer.save()
                except ValidationError as error:
                    testlog.error(error)
                    return Relationship.objects.none()
                except Exception as error:
                    testlog.warning(error)
                    return Relationship.objects.none()
                else:
                    # return objects must be iterable
                    try:
                        Profile.objects.filter(user=user)[0].add_point(30)
                    except Exception as error:
                        testlog.warning(error)
                    return [daily_performer]

    def check_daily(self, user):
        is_performer_drawn = False
        is_all_drawn = False
        try:
            daily_performer = Relationship.objects.filter(
                Q(client=user) | Q(performer=user)).filter(created__date=datetime.date.today()).first()
        except Exception as error:
            testlog.error(error)
            return (is_performer_drawn, is_all_drawn)

        if daily_performer:
            # because if you draw the card, you will always in the client field
            if daily_performer.client == user:
                # already draw daily performer
                is_performer_drawn = True

        own_performer_pk = [user.pk]
        own_relationship = Relationship.objects.filter(client=user)
        for relationship in own_relationship:
            own_performer_pk.append(relationship.performer.pk)
        own_relationship = Relationship.objects.filter(performer=user)
        for relationship in own_relationship:
            own_performer_pk.append(relationship.client.pk)

        try:
            all_performers = User.objects.filter(
                groups__name__exact="Performers").exclude(pk__in=own_performer_pk)
        except Exception as error:
            testlog.error(error)
            return (is_performer_drawn, is_all_drawn)

        if len(all_performers) == 0:
            is_all_drawn = True

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
        verbose_name = 'Relationship'
        verbose_name_plural = 'My Relationships'
        unique_together = ('client', 'performer')
        ordering = ['client', 'performer', '-created']

    def __str__(self):
        return "Client \"%s\" Performer \"%s\"" % (self.client.username, self.performer.username)

    def save(self, *args, **kwargs):
        # Some identity check for the User
        # if not is_client(self.client):
        #     raise ValidationError("self.client is not in Clients Group")
        # if not is_performer(self.performer):
        #     raise ValidationError("self.performer is not in Performers Group")
        if self.client == self.performer:
            raise ValidationError(
                "self.client and slef.performer can't be same person")

        # create unique label used for chatroom
        hashkey = self.client.username + \
            self.performer.username + str(self.created)
        relationship_label = hash(hashkey) % (10 ** 20)
        relationship_label = slugify(relationship_label)
        try:
            self.label = relationship_label
        except Exception as error:
            testlog.error(error)
            relationship_label = hash(hashkey**2) % (10 ** 20)
            relationship_label = slugify(relationship_label)
            self.label = relationship_label

        super(Relationship, self).save(*args, **kwargs)
