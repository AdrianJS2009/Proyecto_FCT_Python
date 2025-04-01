from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from drones.infrastructure.models import Drone, Matrix
import threading


_user = threading.local()


def set_current_user(user):
    _user.value = user


def get_current_user():
    return getattr(_user, "value", None)


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(request.user if request.user.is_authenticated else None)
        response = self.get_response(request)
        return response


def create_log_entry(instance, action_flag, message):
    user = get_current_user()
    if user:
        LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=force_str(instance),
            action_flag=action_flag,
            change_message=message,
        )


@receiver(post_save, sender=Drone)
def log_drone_save(sender, instance, created, **kwargs):
    action = ADDITION if created else CHANGE
    message = "Signal: Drone created" if created else "Signal: Drone updated"
    create_log_entry(instance, action, message)


@receiver(post_delete, sender=Drone)
def log_drone_delete(sender, instance, **kwargs):
    create_log_entry(instance, DELETION, "Signal: Drone deleted")


@receiver(post_save, sender=Matrix)
def log_matrix_save(sender, instance, created, **kwargs):
    action = ADDITION if created else CHANGE
    message = "Signal: Matrix created" if created else "Signal: Matrix updated"
    create_log_entry(instance, action, message)


@receiver(post_delete, sender=Matrix)
def log_matrix_delete(sender, instance, **kwargs):
    create_log_entry(instance, DELETION, "Signal: Matrix deleted")
