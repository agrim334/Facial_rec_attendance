"""empty message

Revision ID: 3b655b340e85
Revises: 9327945a10ef
Create Date: 2020-03-12 12:01:55.625202

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3b655b340e85'
down_revision = '9327945a10ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('attendance', 'Present')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('Present', mysql.VARCHAR(length=4), nullable=True))
    # ### end Alembic commands ###
