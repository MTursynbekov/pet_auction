from celery import shared_task
from django.utils import timezone

from core.models import Lot, Bid
from utils.constants import LOT_STATUS_CLOSED, LOT_STATUS_ACTIVE


def determine_the_winner(lot_id):
    lot = Lot.objects.get(id=lot_id)
    lot.status = LOT_STATUS_CLOSED
    winner_bid = Bid.objects.get(lot_id=lot.id, value=lot.price)
    winner_bid.is_won = True
    winner_bid.owner.profile.balance -= winner_bid.value
    lot.owner.profile.balance += winner_bid.value
    lot.pet.owner = winner_bid.owner
    lot.save()
    winner_bid.save()
    lot.owner.save()
    winner_bid.owner.save()
    lot.pet.save()
    return f'Winner determined: {lot.status}',  \
           f'{winner_bid.is_won}, {winner_bid.owner.profile.balance}',  \
           f'{lot.owner.profile.balance}, {lot.pet.owner}, {lot.pet.name}'


@shared_task
def check_lot_end_date():
    lots = Lot.objects.filter(status=LOT_STATUS_ACTIVE)
    timedelta = timezone.timedelta(minutes=5)
    for lot in lots:
        if timezone.now() - timedelta < lot.end_date < timezone.now() + timedelta:
            return determine_the_winner(lot.id)
    return 'No finished lots'

