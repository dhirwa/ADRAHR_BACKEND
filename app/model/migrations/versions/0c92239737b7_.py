"""empty message

Revision ID: 0c92239737b7
Revises: 1b8cb1f182a1
Create Date: 2017-06-05 12:10:48.915099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c92239737b7'
down_revision = '1b8cb1f182a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'status')
    # ### end Alembic commands ###
