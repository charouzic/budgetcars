import pandas as pd
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.models.car import Car
from app.db.data.parse_cars import parse_car_csv_to_df
from app.models.car import FuelType, Transmission

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    create_first_user(db)
    company_id = get_or_create_company(db)
    branch_id = get_or_create_branch(db, company_id)
    create_first_user_under_company_and_branch(db, company_id, branch_id)
    df_cars = parse_car_csv_to_df()
    upload_cars_df_to_db(db, df_cars, company_id, branch_id)

    
def create_first_user(db: Session) -> None:
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841

def create_first_user_under_company_and_branch(db: Session, company_id: int, branch_id: int) -> None:
    email = "superuser@filuta.ai"
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in = schemas.UserCreate(
            email=email,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            company_id=company_id,
            branch_id=branch_id,
            is_superuser=True,
        )
        user = crud.user.create_with_company_id_and_branch_id(db, obj_in=user_in)  # noqa: F841

def get_or_create_company(db: Session) -> int:
    company = crud.company.get(db, id=1)
    if not company:
        company_in = schemas.CompanyCreate(
            name = "FilutaAI"
        )
        company = crud.company.create(db, obj_in=company_in)  # noqa: F841
        
    return int(company.id)

def get_or_create_branch(db: Session, company_id: int) -> int:
    branch = crud.branch.get_by_company(db, company_id=company_id)
    if not branch:
        branch_in = schemas.BranchCreate(
            company_id = company_id,
            branch_name = "Headquarters",
            location = "Prague"
        )
        branch = crud.branch.create(db, obj_in=branch_in, company_id=company_id)  # noqa: F841

    return int(branch.id)

def upload_cars_df_to_db(db: Session, df: pd.DataFrame, company_id: int, branch_id: int)  -> None:
    car = crud.car.get_all(db, company_id=company_id, branch_id=branch_id, limit=1)
    if not car:
        for _, row in df.iterrows():
            fuel_type_str = row['Fuel Type']
            transmission_str = row['Transmission']

            # Check if fuel_type_str is a valid member of FuelType Enum
            fuel_type = getattr(FuelType, fuel_type_str, FuelType.UNKNOWN)

            # Check if transmission_str is a valid member of Transmission Enum
            transmission = getattr(Transmission, transmission_str, Transmission.UNKNOWN)

            car_data = Car(
                make=row['Make'],
                model=row['Model'],
                price=row['Price'],
                year=row['Year'],
                kilometers=row['Kilometer'],
                fuel_type=fuel_type,
                transmission=transmission,
                color=row['Color'],
                seats=row['Seating Capacity']
            )
            crud.car.create(db=db, company_id=company_id, branch_id=branch_id, obj_in=car_data)
