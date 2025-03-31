
from django.db import models
import enum

class OrientationEnum(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    O = "O"

    # Turn methods


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


# Las opcions van por tuplas (valor, etiqueta)
ORIENTATION_CHOICES = [(tag.value, tag.value) for tag in OrientationEnum]

class Matrix(models.Model):
    max_x = models.PositiveIntegerField()
    max_y = models.PositiveIntegerField()

    def __str__(self):
        return f"Matrix {self.max_x}x{self.max_y}"
    

class Drone(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES)
    matrix = models.ForeignKey(Matrix, related_name="drones", on_delete=models.CASCADE)

    def __str__(self):
        return f"Drone {self.id}: {self.name} ({self.model})"
    
    # Movement methods
    def turn_left(self):
        current = OrientationEnum(self.orientation)
        self.orientation = current.turn_left().value
    
    def turn_right(self):
        current = OrientationEnum(self.orientation)
        self.orientation = current.turn_right().value

    
    def move_forward(self):
        
        if self.orientation == OrientationEnum.N.value:
            new_y = self.y + 1
            new_x = self.x
        elif self.orientation == OrientationEnum.S.value:
            new_y = self.y - 1
            new_x = self.x
        elif self.orientation == OrientationEnum.E.value:
            new_x = self.x + 1
            new_y = self.y
        elif self.orientation == OrientationEnum.O.value:
            new_x = self.x - 1
            new_y = self.y
        else:
            raise ValueError("Orientación inválida")

        # Matrix limits
        if not (0 <= new_x <= self.matrix.max_x and 0 <= new_y <= self.matrix.max_y):
            raise ValueError(f"El drone {self.id} saldría de los límites de la matriz")

        self.x = new_x
        self.y = new_y