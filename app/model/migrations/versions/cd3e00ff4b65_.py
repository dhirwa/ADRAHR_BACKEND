"""empty message

Revision ID: cd3e00ff4b65
Revises: 
Create Date: 2017-04-26 15:58:01.345061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3e00ff4b65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('id_type', sa.String(length=100), nullable=True),
    sa.Column('id_number', sa.String(length=100), nullable=True),
    sa.Column('telephone', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('education', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('nationality', sa.String(length=50), nullable=True),
    sa.Column('cv_link', sa.String(length=200), nullable=True),
    sa.Column('nid_link', sa.String(length=200), nullable=True),
    sa.Column('contract', sa.String(length=200), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('names', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vac_type', sa.String(length=40), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emp_dependant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=True),
    sa.Column('names', sa.String(length=100), nullable=True),
    sa.Column('relation', sa.String(length=100), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['emp_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emp_emergency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=True),
    sa.Column('names', sa.String(length=100), nullable=True),
    sa.Column('relation', sa.String(length=100), nullable=True),
    sa.Column('number', sa.String(length=100), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['emp_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('funding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('donor_id', sa.Integer(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['donor_id'], ['donor.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leave',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=True),
    sa.Column('vacation_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('reason', sa.String(length=100), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['emp_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['vacation_id'], ['vacation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payroll',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('staff_location', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('active_time', sa.DateTime(), nullable=True),
    sa.Column('inactive_time', sa.DateTime(), nullable=True),
    sa.Column('reason', sa.String(length=100), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['emp_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_loc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payroll_id', sa.Integer(), nullable=True),
    sa.Column('expense_reason', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['payroll_id'], ['payroll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    op.drop_table('project_loc')
    op.drop_table('payroll')
    op.drop_table('leave')
    op.drop_table('funding')
    op.drop_table('emp_emergency')
    op.drop_table('emp_dependant')
    op.drop_table('vacation')
    op.drop_table('user')
    op.drop_table('project')
    op.drop_table('employee')
    op.drop_table('donor')
    # ### end Alembic commands ###
