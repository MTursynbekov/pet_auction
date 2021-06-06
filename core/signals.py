from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Bid, Lot


@receiver(post_save, sender=Bid)
def update_lot_price(sender, instance, created, **kwargs):
    if created:
        Lot.objects.filter(id=instance.lot_id).update(price=instance.value)
