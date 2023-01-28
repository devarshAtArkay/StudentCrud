"""added phone_no

Revision ID: ba07a81fbf0d
Revises: ccbf23a4ec4b
Create Date: 2023-01-28 09:25:07.315912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba07a81fbf0d'
down_revision = 'ccbf23a4ec4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('phone_no', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'phone_no')
    # ### end Alembic commands ###