from rest_framework import serializers
from .models import Drone, Matrix, OrientationEnum

# ----------------------------
# Serializers para Matrices
# ----------------------------


class CreateMatrixRequestSerializer(serializers.Serializer):
    max_x = serializers.IntegerField(min_value=1, help_text="Maximum value of the X coordinate")
    max_y = serializers.IntegerField(min_value=1, help_text="Maximum value of the Y coordinate")


class UpdateMatrixRequestSerializer(serializers.Serializer):
    max_x = serializers.IntegerField(min_value=1)
    max_y = serializers.IntegerField(min_value=1)

# ----------------------------
# Serializers para Drones
# ----------------------------

class DroneSerializer(serializers.ModelSerializer):
    # Representa la relación con Matrix mediante su id
    matrix_id = serializers.IntegerField()

    class Meta:
        model = Drone
        fields = ['id', 'name', 'model', 'x', 'y', 'orientation', 'matrix_id']

class MatrixSerializer(serializers.ModelSerializer):
    drones = DroneSerializer(many=True, read_only=True)

    class Meta:
        model = Matrix
        fields = ['id', 'max_x', 'max_y', 'drones']


class DroneSerializer(serializers.ModelSerializer):
    # Representa la relación con Matrix mediante su id
    matrix_id = serializers.IntegerField()

    class Meta:
        model = Drone
        fields = ['id', 'name', 'model', 'x', 'y', 'orientation', 'matrix_id']


class UpdateDroneRequestSerializer(serializers.Serializer):
    matrix_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    orientation = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in OrientationEnum])

class CreateDroneRequestSerializer(serializers.Serializer):
    matrix_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    orientation = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in OrientationEnum])

# ----------------------------
# Serializers para respuestas simples y errores
# ----------------------------


class SimpleResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ApiErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()

# ----------------------------
# Serializers para comandos de vuelo
# ----------------------------


class CommandsRequestSerializer(serializers.Serializer):
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        allow_empty=False
    )


class DroneCommandSerializer(serializers.Serializer):
    drone_id = serializers.IntegerField()
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        allow_empty=False
    )

class BatchDroneCommandRequestSerializer(serializers.Serializer):
    commands = serializers.ListField(child=DroneCommandSerializer())
