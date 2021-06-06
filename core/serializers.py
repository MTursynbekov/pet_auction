from django.utils import timezone
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _
from core.models import Pet, Lot, Bid
from utils.constants import LOT_STATUS_INACTIVE


class PetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        exclude = ('owner',)


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'


class LotCreateSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Lot
        fields = ('pet_id', 'price', 'end_date')

    def validate(self, attr):
        if attr['start_date'] >= attr['end_date']:
            raise serializers.ValidationError(_("the end date of the lot can not be before the start date of the lot"))
        return attr


class LotSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)

    class Meta:
        model = Lot
        exclude = ('owner', )


class BidCreateSerializer(serializers.ModelSerializer):
    lot_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bid
        fields = ('value', 'lot_id')

    def validate(self, attr):
        lot = Lot.objects.get(id=attr['lot_id'])
        owner = self.context['request'].user
        owner_lots = Lot.objects.filter(owner=owner)

        if lot in owner_lots:
            raise serializers.ValidationError(_('You can not bid on your lot'))

        if lot.status == LOT_STATUS_INACTIVE:
            raise serializers.ValidationError(_('The lot is inactive'))

        if lot.end_date > timezone.now():
            raise serializers.ValidationError(_('Lot closed'))

        if attr['value'] > owner.profile.balance:
            raise serializers.ValidationError(_('The bid value can not be greater than the user balance'))

        if attr['value'] <= lot.price:
            raise serializers.ValidationError(_('The bid value must be greater than the lot price'))

        return attr


class BidSerializer(serializers.ModelSerializer):
    lot = LotSerializer()

    class Meta:
        model = Bid
        fields = '__all__'
