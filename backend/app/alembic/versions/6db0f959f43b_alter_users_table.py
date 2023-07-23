"""Alter users table

Revision ID: 6db0f959f43b
Revises: 695a1b7fbd81
Create Date: 2023-07-23 15:16:18.080762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6db0f959f43b'
down_revision = '695a1b7fbd81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('company_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('branch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'companies', ['company_id'], ['id'])
    op.create_foreign_key(None, 'user', 'branches', ['branch_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'branch_id')
    op.drop_column('user', 'company_id')
    # ### end Alembic commands ###