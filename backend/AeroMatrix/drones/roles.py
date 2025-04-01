from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from drones.infrastructure.models import Drone, Matrix

def setup_roles():
    # --- Operator ---
    operador, _ = Group.objects.get_or_create(name="Operator")
    operador.permissions.set([]) 

    # --- Drone Manager ---
    gestor_drones, _ = Group.objects.get_or_create(name="Drone Manager")
    drone_ct = ContentType.objects.get_for_model(Drone)
    permisos_drones = Permission.objects.filter(content_type=drone_ct).exclude(codename__startswith='delete')
    gestor_drones.permissions.set(permisos_drones)

    # --- Supervisor ---
    supervisor, _ = Group.objects.get_or_create(name="Supervisor")
    matrix_ct = ContentType.objects.get_for_model(Matrix)
    permisos_matrices = Permission.objects.filter(content_type=matrix_ct).exclude(codename__startswith='delete')
    supervisor.permissions.set(permisos_matrices)
