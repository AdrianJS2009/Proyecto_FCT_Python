
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status

def get_matrix(db: Session, matrix_id: int):
    matrix = db.query(models.Matrix).filter(models.Matrix.id == matrix_id).first()
    if not matrix:
        raise HTTPException(status_code=404, detail=f"Matrix ID {matrix_id} not found")
    return matrix

def create_drone(db: Session, drone: schemas.DroneCreate):

    matrix = get_matrix(db, drone.matrix_id)
    if drone.x > matrix.max_x or drone.y > matrix.max_y:
        raise HTTPException(status_code=409, detail=f"Invalid coordinates ({drone.x},{drone.y}) for matrix {matrix.id}")
    
    
    db_drone = models.Drone(
        name=drone.name,
        model=drone.model,
        x=drone.x,
        y=drone.y,
        orientation=drone.orientation,
        matrix_id=drone.matrix_id
    )
    db.add(db_drone)
    db.commit()
    db.refresh(db_drone)
    return db_drone


