"""Unique the users.user_id field

Revision ID: 5f9cee34c025
Revises: 6717fdd645be
Create Date: 2023-01-08 12:18:59.261693

Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5f9cee34c025"
down_revision = "6717fdd645be"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["user_id"])

    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("urls", schema=None) as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.drop_constraint("urls_user_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(None, "users", ["owner_id"], ["user_id"])
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("urls", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True)
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key("urls_user_id_fkey", "users", ["user_id"], ["id"])
        batch_op.drop_column("owner_id")

    # ### end Alembic commands ###
