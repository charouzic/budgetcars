from typing import Any, List
from app.core.validators import validate_user_interaction

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/company/{company_id}/branch/{branch_id}/user_interactions/", response_model=List[schemas.UserInteraction])
def read_user_interactions(
    company_id: int,
    branch_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve user interactions for a given company and branch.
    """
    user_interactions = crud.user_interaction.get_multi_by_company_and_branch(db, branch_id=branch_id, company_id=company_id, skip=skip, limit=limit)
    return user_interactions

@router.post("/user_interactions/", response_model=schemas.UserInteraction)
def record_user_interaction(
    *,
    db: Session = Depends(deps.get_db),
    user_interaction_in: schemas.UserInteractionCreate,
) -> Any:
    """
    Records new user interaction.
    """
    
    # Check if the provided branch_id, company_id, car_id, and user_id exist and are associated correctly
    validate_user_interaction(db, user_interaction_in)

    user_interaction = crud.user_interaction.create(db=db, obj_in=user_interaction_in)
    return user_interaction

@router.put("/user_interactions/{interaction_id}", response_model=schemas.UserInteraction)
def update_user_interaction(
    *,
    db: Session = Depends(deps.get_db),
    interaction_id: int,
    user_interaction_in: schemas.UserInteractionUpdate,
) -> Any:
    """
    Update user interaction.
    """
    
    user_interaction = crud.user_interaction.get(db=db, id=interaction_id)
    if not user_interaction:
        raise HTTPException(status_code=404, detail="User interaction not found")
    
    # Check if the provided branch_id, company_id, car_id, and user_id exist and are associated correctly
    validate_user_interaction(db, user_interaction_in)

    user_interaction = crud.user_interaction.update(db=db, db_obj=user_interaction, obj_in=user_interaction_in)
    return user_interaction

@router.get("/user_interactions/{interaction_id}", response_model=schemas.UserInteraction)
def read_user_interaction(
    interaction_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve user interaction by id.
    """
    user_interaction = crud.user_interaction.get(db, id=interaction_id)
    if not user_interaction:
        raise HTTPException(status_code=404, detail="User interaction not found")
    return user_interaction

@router.get("/car/{car_id}/user_interactions/", response_model=List[schemas.UserInteraction])
def read_user_interactions_for_car(
    car_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve user interactions by car id.
    """
    user_interaction = crud.user_interaction.get_multi_by_car(db, car_id=car_id, skip=skip, limit=limit)
    if not user_interaction:
        raise HTTPException(status_code=404, detail="User interaction with the provided car id not found")
    return user_interaction

@router.get("/user/{user_id}/user_interactions/", response_model=List[schemas.UserInteraction])
def read_user_interactions_for_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve user interactions for a given user.
    """
    user_interactions = crud.user_interaction.get_multi_by_user(db, user_id=user_id, skip=skip, limit=limit)
    if not user_interactions:
        raise HTTPException(status_code=404, detail="User interaction with the provided user id not found")
    return user_interactions

@router.delete("/user_interactions/{interaction_id}", response_model=schemas.UserInteraction)
def delete_user_interactions(
    interaction_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve user interaction by id.
    """
    user_interaction = crud.user_interaction.get(db, id=interaction_id)
    if not user_interaction:
        raise HTTPException(status_code=404, detail="User interaction not found")
    user_interaction = crud.user_interaction.remove(db, id=interaction_id)
    return user_interaction