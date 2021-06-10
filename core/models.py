from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utils.constants import KINDS_OF_PET, KIND_OF_PET_CAT, LOT_STATUSES, LOT_STATUS_ACTIVE


def default_end_time():
    now = timezone.now()
    start = now.replace(hour=13, minute=0, second=0, microsecond=0)
    return start + timedelta(days=7)


class Pet(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Pet\'s name'))
    breed = models.CharField(max_length=100, blank=True, verbose_name=_('Pet breed'))
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='pets',
                              blank=True,
                              verbose_name=_('Owner of pet'))
    kind = models.SmallIntegerField(choices=KINDS_OF_PET, default=KIND_OF_PET_CAT, verbose_name=_('Kinds of pet'))

    class Meta:
        verbose_name = _('Pet')
        verbose_name_plural = _('Pets')

    def __str__(self):
        return f'{self.name} - {self.kind}'


class Lot(models.Model):
    pet = models.ForeignKey(Pet,
                            on_delete=models.CASCADE,
                            related_name='lots',
                            blank=True,
                            verbose_name=_('Pet'))
    price = models.FloatField(verbose_name=_('Price of lot'))
    status = models.SmallIntegerField(choices=LOT_STATUSES, default=LOT_STATUS_ACTIVE,
                                      verbose_name=_('Status of the lot'))
    start_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Auction start date'))
    end_date = models.DateTimeField(default=default_end_time, verbose_name=_('Auction end date'))
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='lots',
                              blank=True,
                              verbose_name=_('Owner of lot'))

    class Meta:
        verbose_name = _('Lot')
        verbose_name_plural = _('Lots')

    def __str__(self):
        return f'{self.pet}: {self.price}tg'


class Bid(models.Model):
    value = models.FloatField(verbose_name=_('Bid value'))
    placement_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Bid placement date'))
    is_won = models.BooleanField(default=False, verbose_name=_('Is bid won?'))
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='bids',
                              blank=True,
                              verbose_name=_('Bid owner'))
    lot = models.ForeignKey(Lot,
                            on_delete=models.CASCADE,
                            related_name='bids',
                            blank=True,
                            verbose_name=_('For what lot?'))

    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')

    def __str__(self):
        return f'{self.lot} - RBid: {self.value}'
