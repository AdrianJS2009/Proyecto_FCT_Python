from .models import Drone, Matrix

def find_drones_by_position_and_matrix(x: int, y: int, matrix_id: int):
    return Drone.objects.filter(x=x, y=y, matrix_id=matrix_id)

def find_drones_by_matrix(matrix_id: int):
    return Drone.objects.filter(matrix_id=matrix_id)

def exists_drone_by_model_and_matrix(model: str, matrix_id: int) -> bool:
    return Drone.objects.filter(model=model, matrix_id=matrix_id).exists()

def exists_drone_by_name_and_matrix(name: str, matrix_id: int) -> bool:
    return Drone.objects.filter(name=name, matrix_id=matrix_id).exists()

def find_matrix_by_max_x_and_max_y(max_x: int, max_y: int):
    return Matrix.objects.filter(max_x=max_x, max_y=max_y)
