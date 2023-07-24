# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.user import User  # noqa
from app.models.company import Company  # noqa
from app.models.branch import Branch # noqa
from app.models.car import Car # noqa
from app.models.user_interaction import UserInteraction # noqa
