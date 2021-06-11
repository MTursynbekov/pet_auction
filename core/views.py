from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Pet, Lot, Bid
from core.permissions import IsOwnerOrAdmin
from core.serializers import PetSerializer, PetCreateSerializer, LotSerializer, LotCreateSerializer, BidSerializer, \
    BidCreateSerializer
from utils.constants import LOT_STATUS_ACTIVE, LOT_STATUS_CLOSED


class PetsViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    # restricting object editing to owners and staff only
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return Pet.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PetCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.filter(status=LOT_STATUS_ACTIVE)
    serializer_class = LotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return Lot.objects.filter(owner=self.request.user, status=LOT_STATUS_ACTIVE)

    def get_serializer_class(self):
        if self.action == 'create':
            return LotCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['GET'], detail=True, url_path='bids', permission_classes=[IsOwnerOrAdmin])
    def get_lot_bids(self, request, pk):
        lot_bids = Bid.objects.filter(lot_id=pk)
        serializer = BidSerializer(lot_bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='closed', permission_classes=[IsOwnerOrAdmin])
    def get_closed_lots(self, request):
        closed_lots = Lot.objects.filter(status=LOT_STATUS_CLOSED, owner=request.user)
        serializer = LotSerializer(closed_lots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, url_path='accept_bid', permission_classes=[IsOwnerOrAdmin])
    def accept_the_bid(self, request, pk):
        try:
            lot = Lot.objects.get(id=pk, status=LOT_STATUS_ACTIVE)
        except Lot.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        try:
            winner_bid = Bid.objects.get(id=request.data['bid_id'])
        except Bid.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        winner_bid.is_won = True
        winner_bid.owner.profile.balance -= winner_bid.value
        lot.owner.profile.balance += winner_bid.value
        lot.status = LOT_STATUS_CLOSED
        lot.pet.owner = winner_bid.owner
        lot.save()
        winner_bid.save()
        lot.owner.save()
        winner_bid.owner.save()
        lot.pet.save()
        return Response(f'Winner of lot {lot} determined succesfully!', status=status.HTTP_200_OK)


class BidsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Bid.objects.filter(is_won=False)
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return Bid.objects.filter(owner=self.request.user, is_won=False)

    def get_serializer_class(self):
        if self.action == 'create':
            return BidCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['GET'], detail=False, url_path='won', permission_classes=[IsOwnerOrAdmin])
    def get_won_bids(self, request):
        if request.user.is_staff is False:
            won_bids = Bid.objects.filter(is_won=True, owner=request.user)
        else:
            won_bids = Bid.objects.filter(is_won=True)
        serializer = BidSerializer(won_bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
