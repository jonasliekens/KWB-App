"""added active property to user

Revision ID: 5f9359413469
Revises: 3bd9e44ec844
Create Date: 2017-08-16 13:53:43.797678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f9359413469'
down_revision = '3bd9e44ec844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    # ### end Alembic commands ###
