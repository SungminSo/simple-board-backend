"""empty message

Revision ID: ead5c9af46c9
Revises: 8eb1561da53d
Create Date: 2020-09-06 16:34:33.176463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead5c9af46c9'
down_revision = '8eb1561da53d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'board', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'board', type_='unique')
    # ### end Alembic commands ###
