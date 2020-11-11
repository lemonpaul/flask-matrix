"""empty message

Revision ID: 5578cb0d6cb1
Revises: 
Create Date: 2020-11-11 01:31:36.639432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5578cb0d6cb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('matrices')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('matrices',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('width', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('body', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='matrices_pkey')
    )
    # ### end Alembic commands ###