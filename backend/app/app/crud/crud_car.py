from typing import List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.car import Car, FuelType, Transmission
from app.schemas.car  import CarCreate, CarUpdate

# Define a type variable for the column type
ColumnT = TypeVar('ColumnT')

class CRUDCar(CRUDBase[Car, CarCreate, CarUpdate]):
    def create(self, db: Session, *, obj_in: CarCreate, company_id: int, branch_id: int) -> Car:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, company_id=company_id, branch_id=branch_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Car]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_makes(self, db: Session, company_id: int, branch_id: int) -> List[str]:
        return car.get_distinct_values_from_column(Car.make, db, company_id=company_id, branch_id=branch_id)


    def get_colors(self, db: Session, company_id: int, branch_id: int) -> List[str]:
        return car.get_distinct_values_from_column(Car.color, db, company_id=company_id, branch_id=branch_id)
    
    def get_seats(self, db: Session, company_id: int, branch_id: int) -> List[int]:
        return car.get_distinct_values_from_column(Car.seats, db, company_id=company_id, branch_id=branch_id)
    
    def search_by_filters(
        self,
        db: Session,
        company_id: int,
        branch_id: int,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        fuel_type: Optional[FuelType] = None,
        transmission: Optional[Transmission] = None,
        color: Optional[str] = None,
        seats_min: Optional[int] = None,
        seats_max: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Car]:
        query = db.query(self.model).filter(
            self.model.company_id == company_id,
            self.model.branch_id == branch_id
        )

        # Define a list to store the filter conditions
        filter_conditions = []

        if make:
            filter_conditions.append(self.model.make == make)

        if model:
            filter_conditions.append(self.model.model == model)

        if year_min:
            filter_conditions.append(self.model.year >= year_min)

        if year_max:
            filter_conditions.append(self.model.year <= year_max)

        if price_min:
            filter_conditions.append(self.model.price >= price_min)

        if price_max:
            filter_conditions.append(self.model.price <= price_max)

        if fuel_type:
            filter_conditions.append(self.model.fuel_type == fuel_type.value)

        if transmission:
            filter_conditions.append(self.model.transmission == transmission.value)

        if color:
            filter_conditions.append(self.model.color == color)

        if seats_min:
            filter_conditions.append(self.model.seats >= seats_min)

        if seats_max:
            filter_conditions.append(self.model.seats <= seats_max)

        # Combine all filter conditions using and_
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        return query.offset(skip).limit(limit).all()
    
    def get_distinct_values_from_column(
        self,
        column: Type[ColumnT],
        db: Session,
        company_id: int,
        branch_id: int
    ) -> List[ColumnT]:
        results = db.query(column).filter(
            self.model.company_id == company_id,
            self.model.branch_id == branch_id
        ).distinct().all()

        return [result[0] for result in results]

car = CRUDCar(Car)
