
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('drones.urls')),  # Todas las rutas de la app 'drones' estarán bajo /api/
]
