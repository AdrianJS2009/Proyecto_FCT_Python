from rest_framework import serializers
from ..infrastructure.models import Drone, OrientationEnum


class DroneSerializer(serializers.ModelSerializer):
    matrix_id = serializers.IntegerField()

    class Meta:
        model = Drone
        fields = ['id', 'name', 'model', 'x', 'y', 'orientation', 'matrix_id']


class CreateDroneRequestSerializer(serializers.Serializer):
    matrix_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    orientation = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in OrientationEnum])


class UpdateDroneRequestSerializer(serializers.Serializer):
    matrix_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    orientation = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in OrientationEnum])
