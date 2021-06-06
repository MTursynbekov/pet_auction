from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Pet, Lot, Bid
from core.serializers import PetSerializer, PetCreateSerializer, LotSerializer, LotCreateSerializer, BidSerializer, \
    BidCreateSerializer


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
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return Lot.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LotCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['GET'], detail=True, url_path='bids')
    def get_lot_bids(self, request, pk):
        lot_bids = Bid.objects.filter(lot_id=pk)
        serializer = BidSerializer(lot_bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BidsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return Bid.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BidCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['GET'], detail=False, url_path='won')
    def get_won_bids(self, request):
        won_bids = Bid.objects.filter(is_won=True)
        serializer = BidSerializer(won_bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
