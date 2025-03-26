# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class Orientation(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    O = "O"

    def turn_left(self):
        mapping = {Orientation.N: Orientation.O, Orientation.O: Orientation.S,
                   Orientation.S: Orientation.E, Orientation.E: Orientation.N}
        return mapping[self]

    def turn_right(self):
        mapping = {Orientation.N: Orientation.E, Orientation.E: Orientation.S,
                   Orientation.S: Orientation.O, Orientation.O: Orientation.N}
        return mapping[self]

class Drone(Base):
    __tablename__ = 'drones'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    orientation = Column(Enum(Orientation), nullable=False)
    matrix_id = Column(Integer, ForeignKey('matrix.id'), nullable=False)
    
    # un drone pertenece a una matriz
    matrix = relationship("Matrix", back_populates="drones")

class Matrix(Base):
    __tablename__ = 'matrix'
    
    id = Column(Integer, primary_key=True, index=True)
    max_x = Column(Integer, nullable=False)
    max_y = Column(Integer, nullable=False)
    
    # una matriz tiene muchos drones
    drones = relationship("Drone", back_populates="matrix")
