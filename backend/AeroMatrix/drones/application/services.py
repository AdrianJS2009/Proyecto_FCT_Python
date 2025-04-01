from django.db import transaction
from drones.infrastructure.models import Drone, Matrix, OrientationEnum
from drones.domain.exceptions import ConflictException, NotFoundException, UnsupportedCommandException
from drones.domain.repositories import (
    find_drones_by_position_and_matrix,
    find_drones_by_matrix,
    exists_drone_by_model_and_matrix,
    exists_drone_by_name_and_matrix
)
from rest_framework.exceptions import ValidationError


# -----------------------
# Funciones Helpers
# -----------------------

def validate_position(matrix: Matrix, x: int, y: int):
    if x < 0 or x > matrix.max_x or y < 0 or y > matrix.max_y:
        raise ConflictException(
            f"Invalid coordinates ({x},{y}) for matrix {matrix.id} "
            f"(Max X: {matrix.max_x}, Max Y: {matrix.max_y})"
        )

# -----------------------
# Drone Service
# -----------------------

@transaction.atomic
def create_drone(matrix_id: int, name: str, model: str, x: int, y: int, orientation: str) -> Drone:
    if not name or not name.strip():
        raise ValueError("Drone name must not be empty.")
    if not model or not model.strip():
        raise ValueError("Drone model must not be empty.")
    if orientation is None:
        raise ValueError("Drone orientation must be provided.")

    try:
        matrix = Matrix.objects.get(pk=matrix_id)
    except Matrix.DoesNotExist:
        raise NotFoundException(f"Matrix ID {matrix_id} not found")

    validate_position(matrix, x, y)

    if exists_drone_by_name_and_matrix(name, matrix_id):
        raise ConflictException(f"A drone with the name '{name}' already exists in matrix {matrix_id}")
    if exists_drone_by_model_and_matrix(model, matrix_id):
        raise ConflictException(f"A drone with the model '{model}' already exists in matrix {matrix_id}")
    if find_drones_by_position_and_matrix(x, y, matrix_id).exists():
        raise ConflictException(f"Position conflict at ({x},{y}) in matrix {matrix_id}")

    drone = Drone.objects.create(
        name=name,
        model=model,
        x=x,
        y=y,
        orientation=orientation,
        matrix=matrix
    )
    return drone

@transaction.atomic
def update_drone(drone_id: int, matrix_id: int, name: str, model: str, x: int, y: int, orientation: str) -> Drone:
    validate_drone_inputs(name, model, orientation)

    drone = get_drone_by_id(drone_id)
    new_matrix = get_matrix_by_id(matrix_id)

    validate_position(new_matrix, x, y)
    validate_drone_uniqueness(drone, name, model, matrix_id)
    validate_position_conflict(drone, x, y, matrix_id)
    validate_no_changes(drone, name, model, x, y, orientation, matrix_id)

    update_drone_attributes(drone, new_matrix, name, model, x, y, orientation)
    return drone


def validate_drone_inputs(name: str, model: str, orientation: str):
    if not name or not name.strip():
        raise ValueError("Drone name must not be empty.")
    if not model or not model.strip():
        raise ValueError("Drone model must not be empty.")
    if orientation is None:
        raise ValueError("Drone orientation must be provided.")


def get_drone_by_id(drone_id: int) -> Drone:
    try:
        return Drone.objects.get(pk=drone_id)
    except Drone.DoesNotExist:
        raise NotFoundException(f"Drone ID {drone_id} not found")


def get_matrix_by_id(matrix_id: int) -> Matrix:
    try:
        return Matrix.objects.get(pk=matrix_id)
    except Matrix.DoesNotExist:
        raise NotFoundException(f"Matrix ID {matrix_id} not found")


def validate_drone_uniqueness(drone: Drone, name: str, model: str, matrix_id: int):
    if drone.name != name and exists_drone_by_name_and_matrix(name, matrix_id):
        raise ConflictException(f"A drone with the name '{name}' already exists in matrix {matrix_id}")
    if drone.model != model and exists_drone_by_model_and_matrix(model, matrix_id):
        raise ConflictException(f"A drone with the model '{model}' already exists in matrix {matrix_id}")


def validate_position_conflict(drone: Drone, x: int, y: int, matrix_id: int):
    if ((drone.x != x or drone.y != y or drone.matrix.id != matrix_id) and
            find_drones_by_position_and_matrix(x, y, matrix_id).exists()):
        raise ConflictException(f"Position ({x},{y}) in matrix {matrix_id} is occupied")


def validate_no_changes(drone: Drone, name: str, model: str, x: int, y: int, orientation: str, matrix_id: int):
    if (drone.x == x and drone.y == y and
            drone.orientation == orientation and
            drone.matrix.id == matrix_id and
            drone.name == name and
            drone.model == model):
        raise ConflictException("No changes detected in the drone update.")


def update_drone_attributes(drone: Drone, new_matrix: Matrix, name: str, model: str, x: int, y: int, orientation: str):
    drone.matrix = new_matrix
    drone.x = x
    drone.y = y
    drone.name = name
    drone.model = model
    drone.orientation = orientation
    drone.save()


def delete_drone(drone_id: int) -> Drone:
    try:
        drone = Drone.objects.get(pk=drone_id)
    except Drone.DoesNotExist:
        raise NotFoundException(f"Drone ID {drone_id} not found")
    drone.delete()
    return drone

def get_drone(drone_id: int) -> Drone:
    try:
        return Drone.objects.get(pk=drone_id)
    except Drone.DoesNotExist:
        raise NotFoundException(f"Drone ID {drone_id} not found")

def list_drones():
    return Drone.objects.all()

# -----------------------
# Flight Service
# -----------------------

@transaction.atomic
def execute_commands(drone_id: int, commands: list) -> Drone:
    if not commands:
        raise ValueError("Command list must not be empty.")

    try:
        drone = Drone.objects.select_related('matrix').get(pk=drone_id)
    except Drone.DoesNotExist:
        raise NotFoundException(f"Drone ID {drone_id} not found")

    for cmd in commands:
        if cmd is None:
            raise UnsupportedCommandException("Unsupported command: null")
        if cmd == "TURN_LEFT":
            drone.turn_left()
        elif cmd == "TURN_RIGHT":
            drone.turn_right()
        elif cmd == "MOVE_FORWARD":
            move_forward(drone)
        else:
            raise UnsupportedCommandException(f"Unsupported command: {cmd}")

    drone.save()
    return drone

def execute_commands_in_sequence(drone_ids: list, commands: list):
    for drone_id in drone_ids:
        execute_commands(drone_id, commands)

@transaction.atomic
def execute_batch_commands(batch_commands: list):
    for item in batch_commands:
        drone_id = item.get('drone_id')
        commands = item.get('commands')
        if not commands:
            raise ValueError(f"Drone {drone_id} has no commands to execute.")
        if not Drone.objects.filter(pk=drone_id).exists():
            raise NotFoundException(f"Drone ID {drone_id} not found in batch request.")
        drone = execute_commands(drone_id, commands)
        check_global_collisions(drone)

def move_forward(drone: Drone):
    x, y = drone.x, drone.y
    matrix = drone.matrix

    if drone.orientation == OrientationEnum.N.value:
        y += 1
    elif drone.orientation == OrientationEnum.S.value:
        y -= 1
    elif drone.orientation == OrientationEnum.E.value:
        x += 1
    elif drone.orientation == OrientationEnum.O.value:
        x -= 1

    if x < 0 or x > matrix.max_x or y < 0 or y > matrix.max_y:
        raise ConflictException(
            f"Drone {drone.id} would exit matrix boundaries. New position: ({x},{y}), "
            f"Matrix limits: (0-{matrix.max_x}, 0-{matrix.max_y})"
        )

    others = Drone.objects.filter(x=x, y=y, matrix=matrix)
    if others.exists() and (others.count() > 1 or (others.count() == 1 and others.first().id != drone.id)):
        conflict_drone = others.first()
        raise ConflictException(
            f"Collision detected between drone {drone.id} and drone {conflict_drone.id} at position ({x},{y})"
        )
    drone.x = x
    drone.y = y

def check_global_collisions(drone: Drone):
    drones_in_same_position = Drone.objects.filter(x=drone.x, y=drone.y, matrix=drone.matrix)
    for other in drones_in_same_position:
        if other.id != drone.id:
            raise ConflictException(
                f"Collision detected between drone {drone.id} and drone {other.id}"
            )

# -----------------------
# Matrix Service
# -----------------------

@transaction.atomic
def create_matrix(max_x: int, max_y: int) -> Matrix:
    if max_x is None or max_y is None:
        raise ValidationError("Both max_x and max_y are required.")
    if max_x <= 0 or max_y <= 0:
        raise ValidationError("Matrix dimensions must be greater than 0.")
    
    
    matrix = Matrix.objects.create(max_x=max_x, max_y=max_y)
    return matrix

@transaction.atomic
def update_matrix(matrix_id: int, max_x: int, max_y: int) -> Matrix:
    max_size = 100
    if max_x <= 0 or max_y <= 0:
        raise ConflictException(f"Matrix dimensions must be positive (maxX: {max_x}, maxY: {max_y})")
    if max_x > max_size or max_y > max_size:
        raise ConflictException(f"Matrix dimensions exceed maximum allowed size ({max_size}).")
    try:
        matrix = Matrix.objects.get(pk=matrix_id)
    except Matrix.DoesNotExist:
        raise NotFoundException(f"Matrix ID {matrix_id} not found")

    drones = Drone.objects.filter(matrix=matrix)
    for drone in drones:
        if drone.x >= max_x or drone.y >= max_y:
            raise ConflictException(
                f"Drone {drone.id} is out of bounds for new matrix size (maxX: {max_x}, maxY: {max_y})"
            )

    matrix.max_x = max_x
    matrix.max_y = max_y
    matrix.save()
    return matrix

def get_matrix(matrix_id: int) -> Matrix:
    try:
        return Matrix.objects.get(pk=matrix_id)
    except Matrix.DoesNotExist:
        raise NotFoundException(f"Matrix ID {matrix_id} not found")
    
    

@transaction.atomic
def delete_matrix(matrix_id: int):
    try:
        matrix = Matrix.objects.get(pk=matrix_id)
    except Matrix.DoesNotExist:
        raise NotFoundException(f"Matrix ID {matrix_id} not found")
    drones = Drone.objects.filter(matrix=matrix)
    if drones.exists():
        drone_ids = ", ".join(str(drone.id) for drone in drones)
        raise ConflictException(f"Cannot delete matrix {matrix_id}. Active drones: {drone_ids}")
    matrix.delete()

def list_matrices():
    return Matrix.objects.all()
