from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from pydantic import ValidationError
from app import crud, models, schemas
from app.api import deps
from app.models.car import FuelType, Transmission

router = APIRouter()

@router.get("/company/{company_id}/branch/{branch_id}/cars/", response_model=List[schemas.Car])
def read_cars(
    company_id: int,
    branch_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all cars.
    """
    cars = crud.car.get_all(db, company_id=company_id, 
        branch_id=branch_id, skip=skip, limit=limit)
    return cars

@router.get("/company/{company_id}/branch/{branch_id}/cars/feeling_lucky/", response_model=List[schemas.Car])
def read_cars_feeling_lucky(
    company_id: int,
    branch_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all cars selected randomly.
    """
    cars = crud.car.get_random_records(db, company_id=company_id, 
        branch_id=branch_id, skip=skip, limit=limit)
    return cars


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

@router.get("/car/{id}", response_model=schemas.Car)
def read_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get car by ID.
    """
    car = crud.car.get(db=db, id=id)
    if not car:
        raise HTTPException(status_code=404, detail="Car record not found")
    return car

@router.get("/company/{company_id}/branch/{branch_id}/cars/makes/", response_model=dict)
def read_makes(
    company_id: int,
    branch_id: int,
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all available car makes for a given branch.
    """
    makes = crud.car.get_makes(db=db, company_id=company_id, branch_id=branch_id)
    if not makes:
        raise HTTPException(status_code=404, detail="Makes not found")
    return {"makes": makes}

@router.get("/cars/fuel_types/", response_model=dict)
def read_fuel_types() -> Any:
    """
    Get all available fuel types.
    """
    return {"fuel_types": [fuel_type.value for fuel_type in FuelType]}

@router.get("/cars/transmissions/", response_model=dict)
def read_transmissions() -> Any:
    """
    Get all available transmissions.
    """
    return {"transmissions": [transmission.value for transmission in Transmission]}

@router.get("/company/{company_id}/branch/{branch_id}/cars/colors/", response_model=dict)
def read_colors(
    company_id: int,
    branch_id: int,
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all available car colors for a given branch.
    """
    colors = crud.car.get_colors(db=db, company_id=company_id, branch_id=branch_id)
    if not colors:
        raise HTTPException(status_code=404, detail="Colors not found")
    return {"colors": colors}

# seats
@router.get("/company/{company_id}/branch/{branch_id}/cars/seats/", response_model=dict)
def read_seats(
    company_id: int,
    branch_id: int,
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all available number of seats for a car in a given branch.
    """
    seats = crud.car.get_seats(db=db, company_id=company_id, branch_id=branch_id)
    if not seats:
        raise HTTPException(status_code=404, detail="Seats not found")
    return {"seats": seats}