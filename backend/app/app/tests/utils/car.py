from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app import crud
from app.schemas.car import CarCreate
from app.models.car import Car

def create_test_cars(db: Session, car_data: List[CarCreate], company_id: int, branch_id: int) -> List[Car]:
    created_cars = []
    for car_info in car_data:
        created_car = crud.car.create(db=db, company_id=company_id, branch_id=branch_id, obj_in=car_info)
        created_cars.append(created_car)
    return created_cars
