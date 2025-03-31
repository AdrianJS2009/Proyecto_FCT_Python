from django.contrib import admin
from drones.infrastructure.models import Drone, Matrix

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "x", "y", "orientation", "matrix")
    search_fields = ("name", "model")
    list_filter = ("orientation", "matrix")

@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ("id", "max_x", "max_y")
