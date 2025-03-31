# drones/interfaces/command_serializers.py

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

class BulkCommandSerializer(serializers.Serializer):
    drone_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="IDs of the drones to execute the same sequence of commands"
    )
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        help_text="Sequence of commands to execute on all provided drones"
    )

class MultiDroneCommandRequestSerializer(serializers.Serializer):
    drone_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="List of drone IDs to apply the same commands to"
    )
    commands = serializers.ListField(
        child=serializers.ChoiceField(choices=["TURN_LEFT", "TURN_RIGHT", "MOVE_FORWARD"]),
        allow_empty=False
    )

