from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path

from auth_.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('login/', obtain_jwt_token),
]