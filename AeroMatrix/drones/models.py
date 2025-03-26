
from django.db import models
import enum

class OrientationEnum(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    O = "O"

    # Métodos para girar 
    def turn_left(self):
        mapping = {
            OrientationEnum.N: OrientationEnum.O,
            OrientationEnum.O: OrientationEnum.S,
            OrientationEnum.S: OrientationEnum.E,
            OrientationEnum.E: OrientationEnum.N,
        }
        return mapping[self]

    def turn_right(self):
        mapping = {
            OrientationEnum.N: OrientationEnum.E,
            OrientationEnum.E: OrientationEnum.S,
            OrientationEnum.S: OrientationEnum.O,
            OrientationEnum.O: OrientationEnum.N,
        }
        return mapping[self]

# Para definir choices en un campo de Django, creamos una lista de tuplas
ORIENTATION_CHOICES = [(tag.value, tag.value) for tag in OrientationEnum]
