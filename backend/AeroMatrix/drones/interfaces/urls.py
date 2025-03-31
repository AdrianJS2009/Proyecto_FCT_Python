from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DroneViewSet, MatrixViewSet, FlightView, BatchCommandView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = DefaultRouter()
router.register(r'drones', DroneViewSet, basename='drone')
router.register(r'matrices', MatrixViewSet, basename='matrix')

urlpatterns = [

    path('', include(router.urls)),
    
    path('flights/drones/commands/', FlightView.as_view(), name='flight-commands'),
    
    path('flights/batch-commands/', BatchCommandView.as_view(), name='batch-commands'),
    
  
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
