from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse
)
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
@extend_schema_view(
    list=extend_schema(
        summary="List Drones",
        description="Retrieves the complete list of drones registered in the system.",
        responses=DroneSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Get Drone",
        description="Retrieves the information of a specific drone by its ID.",
        responses=DroneSerializer
    ),
    create=extend_schema(
        summary="Create Drone",
        description="Creates a new drone using the provided data.",
        request=DroneSerializer,
        responses={201: DroneSerializer}
    ),
    update=extend_schema(
        summary="Update Drone",
        description="Updates the information of an existing drone identified by its ID.",
        request=DroneSerializer,
        responses=DroneSerializer
    ),
    destroy=extend_schema(
        summary="Delete Drone",
        description="Deletes a drone from the system.",
        responses={200: OpenApiResponse(description="Drone successfully deleted.")}
    ),
    execute_commands=extend_schema(
        summary="Execute Commands on Drone",
        description="Sends a sequence of movement commands to a specific drone.",
        request=CommandsRequestSerializer,
        responses=DroneSerializer
    )
)
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
@extend_schema(
    summary="Execute Sequential Commands for Multiple Drones",
    description="Executes a sequence of commands on multiple drones at once. Drone IDs are passed as query parameters.",
    request=CommandsRequestSerializer,
    responses={200: OpenApiResponse(description="Commands executed successfully.")}
)
class FlightView(APIView):
    def post(self, request):
        drone_ids = request.query_params.getlist('droneIds')
        serializer = CommandsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commands = serializer.validated_data['commands']

        # Convertir los IDs a enteros
        drone_ids = list(map(int, drone_ids))
        execute_commands_in_sequence(drone_ids, commands)
        return Response(status=status.HTTP_200_OK)


# --- Batch Command Controller ---
@extend_schema(
    summary="Execute Batch Commands for Multiple Drones",
    description="Executes different sequences of commands for various drones in a single request.",
    request=BatchDroneCommandRequestSerializer,
    responses={202: OpenApiResponse(description="Commands accepted and in execution process.")}
)
class BatchCommandView(APIView):
    def post(self, request):
        serializer = BatchDroneCommandRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch_data = serializer.validated_data['commands']
        execute_batch_commands(batch_data)
        return Response(status=status.HTTP_202_ACCEPTED)


# --- Matrix Controller ---
@extend_schema_view(
    list=extend_schema(
        summary="List Matrices",
        description="Retrieves the complete list of registered flight matrices.",
        responses=MatrixSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Get Matrix",
        description="Retrieves the information of a specific matrix by its ID.",
        responses=MatrixSerializer
    ),
    create=extend_schema(
        summary="Create Matrix",
        description="Creates a new matrix with the specified boundaries.",
        request=MatrixSerializer,
        responses={201: MatrixSerializer}
    ),
    update=extend_schema(
        summary="Update Matrix",
        description="Updates the boundaries of an existing matrix.",
        request=MatrixSerializer,
        responses=MatrixSerializer
    ),
    destroy=extend_schema(
        summary="Delete Matrix",
        description="Deletes a matrix as long as it has no associated drones.",
        responses={204: OpenApiResponse(description="Matrix successfully deleted.")}
    )
)
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
