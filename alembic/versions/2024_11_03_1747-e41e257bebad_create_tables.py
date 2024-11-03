"""create tables

Revision ID: e41e257bebad
Revises: 
Create Date: 2024-11-03 17:47:33.914729

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e41e257bebad"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tickers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("price", sa.String(), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tickers")),
    )
    op.create_index(
        op.f("ix_tickers_currency"), "tickers", ["currency"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tickers_currency"), table_name="tickers")
    op.drop_table("tickers")
    # ### end Alembic commands ###
