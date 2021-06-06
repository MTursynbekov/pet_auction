from rest_framework import routers

from core.views import PetsViewSet, LotsViewSet, BidsViewSet

router = routers.DefaultRouter()
router.register(r'pets', PetsViewSet)
router.register(r'lots', LotsViewSet)
router.register(r'bids', BidsViewSet)

urlpatterns = router.urls
