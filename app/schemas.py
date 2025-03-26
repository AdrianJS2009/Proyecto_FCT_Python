
from pydantic import BaseModel, Field
from typing import Optional
import enum

class OrientationEnum(str, enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    O = "O"

class DroneBase(BaseModel):
    name: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    orientation: OrientationEnum

class DroneCreate(DroneBase):
    matrix_id: int

class DroneUpdate(DroneBase):
    matrix_id: int

class Drone(DroneBase):
    id: int
    matrix_id: int

    class Config:
        orm_mode = True

class MatrixBase(BaseModel):
    max_x: int = Field(..., gt=0)
    max_y: int = Field(..., gt=0)

class MatrixCreate(MatrixBase):
    pass

class Matrix(MatrixBase):
    id: int
    drones: list[Drone] = []

    class Config:
        orm_mode = True
