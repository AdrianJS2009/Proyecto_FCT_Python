from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Drone, Matrix
from .serializers import (
    DroneSerializer, 
    MatrixSerializer, 
    CommandsRequestSerializer, 
    BatchDroneCommandRequestSerializer
)
from .services import (
    create_drone,
    get_drone,
    update_drone,
    delete_drone,
    list_drones,
    execute_commands,
    execute_commands_in_sequence,
    execute_batch_commands,
    get_matrix,
    create_matrix,
    update_matrix,
    delete_matrix,
    list_matrices
)

# --- Drone Controller ---
class DroneViewSet(viewsets.ViewSet):
 

    def list(self, request):
        drones = list_drones()
        serializer = DroneSerializer(drones, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        drone = get_drone(int(pk))
        serializer = DroneSerializer(drone)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        drone = create_drone(
            matrix_id=data.get('matrix_id'),
            name=data.get('name'),
            model=data.get('model'),
            x=data.get('x'),
            y=data.get('y'),
            orientation=data.get('orientation')
        )
        serializer = DroneSerializer(drone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        drone = update_drone(
            drone_id=int(pk),
            matrix_id=data.get('matrix_id'),
            name=data.get('name'),
            model=data.get('model'),
            x=data.get('x'),
            y=data.get('y'),
            orientation=data.get('orientation')
        )
        serializer = DroneSerializer(drone)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        drone = delete_drone(int(pk))
        return Response({"message": f"Drone ID {drone.id} deleted."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def execute_commands(self, request, pk=None):
      
        serializer = CommandsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commands = serializer.validated_data['commands']
        drone = execute_commands(int(pk), commands)
        return Response(DroneSerializer(drone).data)


# --- Flight Controller ---
class FlightView(APIView):

    def post(self, request):
        drone_ids = request.query_params.getlist('droneIds')
        serializer = CommandsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commands = serializer.validated_data['commands']

        # Convertir a enteros
        drone_ids = list(map(int, drone_ids))
        execute_commands_in_sequence(drone_ids, commands)
        return Response(status=status.HTTP_200_OK)


# --- Batch Command Controller ---
class BatchCommandView(APIView):
   
    def post(self, request):
        serializer = BatchDroneCommandRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch_data = serializer.validated_data['commands']
        execute_batch_commands(batch_data)
        return Response(status=status.HTTP_202_ACCEPTED)


# --- Matrix Controller ---
class MatrixViewSet(viewsets.ViewSet):
 

    def list(self, request):
        matrices = list_matrices()
        serializer = MatrixSerializer(matrices, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        matrix = get_matrix(int(pk))
        serializer = MatrixSerializer(matrix)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        matrix = create_matrix(max_x=data.get('max_x'), max_y=data.get('max_y'))
        serializer = MatrixSerializer(matrix)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        matrix = update_matrix(matrix_id=int(pk), max_x=data.get('max_x'), max_y=data.get('max_y'))
        serializer = MatrixSerializer(matrix)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        delete_matrix(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
