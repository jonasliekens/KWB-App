"""empty message

Revision ID: 7fc22b5536bf
Revises: 142c4f8d4453
Create Date: 2017-09-08 12:05:03.543006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc22b5536bf'
down_revision = '142c4f8d4453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('location', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'location')
    # ### end Alembic commands ###
