from .crud_item import item
from .crud_user import user
from .crud_company import company
from .crud_branch import branch
from .crud_car import car

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
