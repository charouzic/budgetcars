from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.car import FuelType, Transmission

router = APIRouter()

@router.get("/company/{company_id}/branch/{branch_id}/cars/search/", response_model=List[schemas.Car])
def search_cars(
    company_id: int,
    branch_id: int,
    make: str = Query(None, alias="make"),
    model: str = Query(None, alias="model"),
    year_min: int = Query(None, alias="year_min"),
    year_max: int = Query(None, alias="year_max"),
    price_min: float = Query(None, alias="price_min"),
    price_max: float = Query(None, alias="price_max"),
    fuel_type: str = Query(None, alias="fuel_type"), # cannot be FuelType enum due to pydantic
    transmission: str = Query(None, alias="transmission"), # cannot be Transmission enum due to pydantic
    color: str = Query(None, alias="color"),
    seats_min: int = Query(None, alias="seats_min"),
    seats_max: int = Query(None, alias="seats_max"),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    filters = {
        "make": make,
        "model": model,
        "year_min": year_min,
        "year_max": year_max,
        "price_min": price_min,
        "price_max": price_max,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "color": color,
        "seats_min": seats_min,
        "seats_max": seats_max,
    }

    cars = crud.car.search_by_filters(
        db=db, 
        company_id=company_id, 
        branch_id=branch_id, 
        **filters,
        skip=skip,
        limit=limit
    )
    return cars

@router.post("/company/{company_id}/branch/{branch_id}/cars/", response_model=schemas.Car)
def create_car(
    company_id: int,
    branch_id: int,
    car_data: schemas.CarCreate,
    db: Session = Depends(deps.get_db)
):
    car = crud.car.create(db=db, company_id=company_id, branch_id=branch_id, obj_in=car_data)
    return car



