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
        own_HoldingVocher = HoldingVocher.objects.filter(user=user)
        try:
            daily_vocher = own_HoldingVocher.filter(
                created__date=datetime.date.today()).first()
        except Exception as error:
            testlog.error(error)
            return HoldingVocher.objects.none()

        if daily_vocher:
            # 先檢查今天有沒有抽過，有的話直接return
            return [daily_vocher]
        else:
            # 把限額已經抽完的優惠券加到 unavailable_vocher_pk
            all_vochers = Vocher.objects.all()
            unavailable_vocher_pk = []

            for vocher in all_vochers:
                if vocher.category == 2:
                    # 每週限制
                    if len(HoldingVocher.objects.filter(vocher=vocher, created__week=datetime.date.today().isocalendar()[1])) >= vocher.limit:
                        unavailable_vocher_pk.append(vocher.pk)

                elif vocher.category == 3:
                    # 總數限制
                    if len(HoldingVocher.objects.filter(vocher=vocher)) >= vocher.limit:
                        unavailable_vocher_pk.append(vocher.pk)

            try:
                # available_vochers 是還有限額的優惠券（包含無限額的）
                available_vochers = Vocher.objects.exclude(
                    pk__in=unavailable_vocher_pk)
            except Exception as error:
                testlog.error(error)
                undraw_vochers = []

            num_available_vochers = len(available_vochers)
            if num_available_vochers <= 0:
                all_vochers = Vocher.objects.all()
                if(len(all_vochers) != len(own_HoldingVocher)):
                    testlog.warning(
                        "Error because all vohcers are drawed, but amount not equal to all vochers")

                # 都沒有剩餘有限額可以抽的優惠券，回傳空陣列
                return HoldingVocher.objects.none()

            else:
                candidate_vochers = []
                limit_vocher = []
                week_limit_vocher = []
                normal_vocher = []

                # 先把已經抽過的優惠券從available_vochers剔除，然後存到candidate_vochers
                # 避免使用這一直抽到同樣的優惠券
                already_drawn_vochers_pk = []
                already_drawn_vochers = HoldingVocher.objects.filter(user=user)
                for already_drawn in already_drawn_vochers:
                    already_drawn_vochers_pk.append(already_drawn.vocher.pk)
                candidate_vochers = available_vochers.exclude(
                    pk__in=already_drawn_vochers_pk)

                # 幫優惠券分級
                limit_vocher = candidate_vochers.filter(category=3)
                week_limit_vocher = candidate_vochers.filter(category=2)
                normal_vocher = candidate_vochers.filter(category=1)

                # 抽優惠券
                if len(limit_vocher) > 0 and random.uniform(0, 1) < len(limit_vocher) / 50000:
                    vocher = limit_vocher[random.randint(
                        0, len(limit_vocher) - 1)]

                elif len(week_limit_vocher) > 0 and random.uniform(0, 1) < len(week_limit_vocher) / 1000:
                    vocher = week_limit_vocher[random.randint(
                        0, len(week_limit_vocher) - 1)]

                elif len(normal_vocher) > 0:
                    vocher = normal_vocher[random.randint(
                        0, len(normal_vocher) - 1)]
                else:
                    # candidate_vochers數量為零
                    # 代表有剩限額的優惠券，可是都是已經有抽過了
                    # 再從available_vochers裡面抽
                    vocher = available_vochers[random.randint(
                        0, len(available_vochers) - 1)]

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
                    return [daily_vocher]

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
    bg_url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    show = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.title


VOCHER_LIMIT_CHOICE = (
    (1, "無限制"),
    (2, "每週限制"),
    (3, "總數限制")
)


class Vocher(models.Model):
    title = models.TextField(blank=False, default="Vocher")
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    description = models.TextField(null=True, blank=True)
    due_time = models.DateTimeField(default=timezone.now)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE)

    category = models.PositiveSmallIntegerField(
        default=1, choices=VOCHER_LIMIT_CHOICE)

    limit = models.IntegerField(
        default=0,
        blank=True,
        help_text="Only required if 'category' is 每週限制 or 總數限制.")

    def __str__(self):
        return "%s  %s" % (self.store, self.title)


class HoldingVocher(models.Model):
    vocher = models.ForeignKey(
        Vocher, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    be_used = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    label = models.SlugField(unique=True, blank=True)

    objects = HoldingVocherManager()

    class Meta:
        ordering = ['user', 'vocher', 'be_used', '-created']

    def __str__(self):
        return "%s have %s" % (self.user, self.vocher)

    def reset(self):
        self.created = timezone.now
        self.be_used = False
        self.save()

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
