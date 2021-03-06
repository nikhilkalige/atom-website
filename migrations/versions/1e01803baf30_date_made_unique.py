"""date made unique

Revision ID: 1e01803baf30
Revises: e320ceca408
Create Date: 2014-09-27 00:28:06.678091

"""

# revision identifiers, used by Alembic.
revision = '1e01803baf30'
down_revision = 'e320ceca408'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'downloads', ['date'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'downloads')
    ### end Alembic commands ###
