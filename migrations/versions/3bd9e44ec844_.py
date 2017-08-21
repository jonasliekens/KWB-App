"""empty message

Revision ID: 3bd9e44ec844
Revises: f516e30ab420
Create Date: 2017-08-16 13:50:48.027782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bd9e44ec844'
down_revision = 'f516e30ab420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('firstName', table_name='user')
    op.drop_index('lastName', table_name='user')
    op.drop_index('phone', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('phone', 'user', ['phone'], unique=True)
    op.create_index('lastName', 'user', ['lastName'], unique=True)
    op.create_index('firstName', 'user', ['firstName'], unique=True)
    # ### end Alembic commands ###
