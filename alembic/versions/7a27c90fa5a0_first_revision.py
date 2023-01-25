"""first revision

Revision ID: 7a27c90fa5a0
Revises: 
Create Date: 2023-01-25 10:07:59.380436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a27c90fa5a0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "student",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=True),
        sa.Column("last_name", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("roll_no", sa.String(length=10), nullable=True),
        sa.Column(
            "gender",
            sa.Enum("Male", "Female", "Other", name="genderenum"),
            nullable=True,
        ),
        sa.Column("class_no", sa.INTEGER(), nullable=True),
        sa.Column("stream", sa.String(length=20), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("student")
    # ### end Alembic commands ###