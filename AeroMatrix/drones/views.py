from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Drone, Matrix, OrientationEnum
from .serializers import DroneSerializer, MatrixSerializer
from django.shortcuts import get_object_or_404

# ModelViewSet is a class that provides CRUD operations by default
class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    # Flight control Endpoints
    @action(detail=True, methods=['post'])
    def execute_commands(self, request, pk=None):
        drone = self.get_object()
        commands = request.data.get('commands', [])
        if not commands:
            return Response({"detail": "La lista de comandos no puede estar vacía."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            for cmd in commands:
                if cmd == "TURN_LEFT":
                    drone.turn_left()
                elif cmd == "TURN_RIGHT":
                    drone.turn_right()
                elif cmd == "MOVE_FORWARD":
                    drone.move_forward()
                else:
                    return Response({"detail": f"Comando '{cmd}' no soportado."}, status=status.HTTP_400_BAD_REQUEST)
            drone.save()
            serializer = self.get_serializer(drone)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)


class MatrixViewSet(viewsets.ModelViewSet):
    queryset = Matrix.objects.all()
    serializer_class = MatrixSerializer

