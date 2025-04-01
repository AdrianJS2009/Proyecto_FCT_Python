from django.apps import AppConfig


class DronesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drones'

    def ready(self):
        from .roles import setup_roles
        setup_roles()
        import drones.utils.audit
