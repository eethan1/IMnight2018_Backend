from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError


import datetime
import random
import logging
testlog = logging.getLogger('testdevelop')


class HoldingVocherManager(models.Manager):
    def used_vocher(self, user, label):
        holdingVochers = HoldingVocher.objects.filter(
            user=user).filter(label=label)
        for vocher in holdingVochers:
            try:
                vocher.used()
                return True
            except BaseException as error:
                testlog.error(error)

        return False

    def get_vochers(self, user, storename=None):
        try:
            holdingVochers = HoldingVocher.objects.filter(user=user)
        except Exception as error:
            testlog.error(error)
            return HoldingVocher.objects.none()
        else:
            if storename is not None:
                store = Store.objects.filter(storename=storename)
                vochers = Vocher.objects.filter(store__in=store)
                holdingVochers = holdingVochers.filter(vocher__in=vochers)

            return holdingVochers

    def get_daily(self, user):
        try:
            daily_vocher = HoldingVocher.objects.filter(
                user=user).filter(created__date=datetime.date.today())
        except Exception as error:
            testlog.error(error)
            return HoldingVocher.objects.none()

        if daily_vocher:
            return daily_vocher
        else:
            own_HoldingVocher = HoldingVocher.objects.filter(user=user)
            own_vocher_pk = []
            for holdingVocher in own_HoldingVocher:
                own_vocher_pk.append(holdingVocher.vocher.pk)

            try:
                remain_vochers = Vocher.objects.exclude(
                    pk__in=own_vocher_pk)
            except Exception as error:
                testlog.error(error)
                remain_vochers = []

            num = len(remain_vochers)
            # check if already draw all performers
            if num <= 0:
                vochers = HoldingVocher.objects.filter(user=user)
                error_vochers = vochers.filter(be_used=False)
                if(len(error_vochers) > 0):
                    for error_vocher in error_vochers:
                        error_vocher.used = True
                    testlog.warning(
                        "Error because all vohcers are drawed, but there still some HoldingVocher.used=False")

                all_vochers = Vocher.objects.all()
                if(len(all_vochers) != len(vochers)):
                    testlog.warning(
                        "Error because all vohcers are drawed, but amount not equal to all vochers")

                vochers_num = len(vochers)
                index = random.randint(0, vochers_num - 1)
                daily_vocher = vochers[index]
                daily_vocher.reset()
                # return objects must be iterable
                daily_vocher = [daily_vocher]
                return daily_vocher

            else:
                index = random.randint(0, num - 1)
                vocher = remain_vochers[index]

                try:
                    daily_vocher = self.create(
                        vocher=vocher, user=user)
                    daily_vocher.save()
                except ValidationError as error:
                    testlog.error(error)
                    return HoldingVocher.objects.none()
                except Exception as error:
                    testlog.warning(error)
                    return HoldingVocher.objects.none()
                else:
                    # return objects must be iterable
                    daily_vocher = [daily_vocher]
                    return daily_vocher

    def check_daily(self, user):
        try:
            daily_vocher = HoldingVocher.objects.filter(
                user=user).filter(created__date=datetime.date.today())
        except Exception as error:
            testlog.error(error)
            return False
        if daily_vocher:
            return True
        else:
            return False


class Store(models.Model):
    title = models.TextField(blank=False, default="Store")
    sub_title = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")

    def __str__(self):
        return self.title


class Vocher(models.Model):
    title = models.TextField(blank=False, default="Vocher")
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    description = models.TextField(null=True, blank=True)
    due_time = models.DateTimeField(default=timezone.now)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE)

    def __str__(self):
        return "%s  %s" % (self.store, self.title)


class HoldingVocher(models.Model):
    vocher = models.ForeignKey(
        Vocher, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    be_used = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    label = models.SlugField(unique=True)

    objects = HoldingVocherManager()

    def __str__(self):
        return "%s have %s" % (self.user, self.vocher)

    def reset(self):
        self.created = timezone.now
        self.be_used = False

    def used(self):
        if(self.be_used != False):
            raise Exception("A Vocher can't used twice")
        else:
            self.be_used = True
            self.save()

    def save(self, *args, **kwargs):
        # create unique label used for chatroom
        hashkey = self.user.username + self.vocher.title + str(self.created)
        holdingVocher_label = hash(hashkey) % (10 ** 20)
        holdingVocher_label = slugify(holdingVocher_label)
        try:
            self.label = holdingVocher_label
        except Exception as error:
            testlog.error(error)
            holdingVocher_label = hash(hashkey**2) % (10 ** 20)
            holdingVocher_label = slugify(holdingVocher_label)
            self.label = holdingVocher_label

        super(HoldingVocher, self).save(*args, **kwargs)
