from rest_framework import serializers


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
