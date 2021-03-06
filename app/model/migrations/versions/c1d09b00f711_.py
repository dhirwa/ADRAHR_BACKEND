"""empty message

Revision ID: c1d09b00f711
Revises: 9d0cd8cfec8d
Create Date: 2017-05-31 18:00:47.958675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d09b00f711'
down_revision = '9d0cd8cfec8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('manager', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employee', 'employee', ['manager'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_column('employee', 'manager')
    # ### end Alembic commands ###
