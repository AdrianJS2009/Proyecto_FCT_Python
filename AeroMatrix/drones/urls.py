from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DroneViewSet, MatrixViewSet

router = DefaultRouter()
router.register(r'drones', DroneViewSet)
router.register(r'matrices', MatrixViewSet)

urlpatterns = [
    path('', include(router.urls)),
]