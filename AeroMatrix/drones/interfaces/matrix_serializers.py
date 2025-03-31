from rest_framework import serializers
from ..infrastructure.models import Matrix, Drone
from .drone_serializers import DroneSerializer


class CreateMatrixRequestSerializer(serializers.Serializer):
    max_x = serializers.IntegerField(min_value=1, help_text="Maximum value of the X coordinate")
    max_y = serializers.IntegerField(min_value=1, help_text="Maximum value of the Y coordinate")


class UpdateMatrixRequestSerializer(serializers.Serializer):
    max_x = serializers.IntegerField(min_value=1)
    max_y = serializers.IntegerField(min_value=1)


class MatrixSerializer(serializers.ModelSerializer):
    drones = DroneSerializer(many=True, read_only=True)

    class Meta:
        model = Matrix
        fields = ['id', 'max_x', 'max_y', 'drones']

def validate_max_x(self, value):
    if value <= 0:
        raise serializers.ValidationError("max_x must be greater than 0.")
    return value
