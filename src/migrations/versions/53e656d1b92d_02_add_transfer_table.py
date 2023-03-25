"""02_add_transfer_table

Revision ID: 53e656d1b92d
Revises: 74463d7e98f7
Create Date: 2023-03-20 20:20:15.052709

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "53e656d1b92d"
down_revision = "74463d7e98f7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transfer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column("client_host", sa.String(length=40), nullable=True),
        sa.Column("link_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["link.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transfer_date"), "transfer", ["date"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_transfer_date"), table_name="transfer")
    op.drop_table("transfer")
    # ### end Alembic commands ###
