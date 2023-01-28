"""changed phone_no column

Revision ID: 1573263c18d4
Revises: 70e5c8b41701
Create Date: 2023-01-28 10:33:34.009858

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1573263c18d4'
down_revision = '70e5c8b41701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('phone_num', sa.String(length=13), nullable=True))
    op.drop_column('student', 'phone_no')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('phone_no', mysql.VARCHAR(length=10), nullable=True))
    op.drop_column('student', 'phone_num')
    # ### end Alembic commands ###