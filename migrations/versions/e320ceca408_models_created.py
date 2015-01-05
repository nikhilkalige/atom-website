"""models created

Revision ID: e320ceca408
Revises: None
Create Date: 2014-09-26 23:57:15.239052

"""

# revision identifiers, used by Alembic.
revision = 'e320ceca408'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('downloads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('downloads', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('downloads')
    op.drop_table('package')
    ### end Alembic commands ###
