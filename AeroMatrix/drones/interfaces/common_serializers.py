from rest_framework import serializers


class SimpleResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ApiErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()
