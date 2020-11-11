"""empty message

Revision ID: 83b556042f0e
Revises: 87e9d6daa063
Create Date: 2020-11-12 01:07:43.627260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83b556042f0e'
down_revision = '87e9d6daa063'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('l_class', sa.Column('d_class_Id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'l_class', 'd_class', ['d_class_Id'], ['id'])
    op.add_column('r_class', sa.Column('d_class_Id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'r_class', 'd_class', ['d_class_Id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'r_class', type_='foreignkey')
    op.drop_column('r_class', 'd_class_Id')
    op.drop_constraint(None, 'l_class', type_='foreignkey')
    op.drop_column('l_class', 'd_class_Id')
    # ### end Alembic commands ###
