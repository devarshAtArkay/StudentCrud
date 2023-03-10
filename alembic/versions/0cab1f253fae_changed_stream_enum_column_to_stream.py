"""changed stream_enum column to stream

Revision ID: 0cab1f253fae
Revises: 3c41204cf2c5
Create Date: 2023-01-25 10:50:20.856535

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0cab1f253fae"
down_revision = "3c41204cf2c5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "student",
        sa.Column(
            "streams",
            sa.Enum("Commerce", "Science", "Arts", name="streamenum"),
            nullable=True,
        ),
    )
    op.drop_column("student", "stream_enum")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "student",
        sa.Column(
            "stream_enum", mysql.ENUM("Commerce", "Science", "Arts"), nullable=True
        ),
    )
    op.drop_column("student", "streams")
    # ### end Alembic commands ###
