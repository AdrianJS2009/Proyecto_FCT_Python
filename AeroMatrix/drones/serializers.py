from rest_framework import serializers
from .models import Drone, Matrix, ORIENTATION_CHOICES

class MatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matrix
        fields = ["id", "max_x", "max_y"]

class DroneSerializer(serializers.ModelSerializer):
    matrix_id = serializers.IntegerField()

    class Meta:
        model = Drone
        fields = ['id', 'name', 'model', 'x', 'y', 'orientation', 'matrix_id'] 
        extra_kwargs = {
            'name': {'max_length': 50},
            'model': {'max_length': 50},
        }



class DroneCommandSerializer(serializers.Serializer):
    drone_id = serializers.IntegerField()
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        allow_empty=False
    )

class BatchDroneCommandRequestSerializer(serializers.Serializer):
    commands = serializers.ListField(child=DroneCommandSerializer())


class CommandsRequestSerializer(serializers.Serializer):
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        allow_empty=False
    )
