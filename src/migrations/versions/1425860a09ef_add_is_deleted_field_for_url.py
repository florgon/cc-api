"""Add is_deleted field for url

Revision ID: 1425860a09ef
Revises: 06e067e43a7f
Create Date: 2022-12-24 16:30:45.752348

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
revision = "1425860a09ef"
down_revision = "06e067e43a7f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("url", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_deleted", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("url", schema=None) as batch_op:
        batch_op.drop_column("is_deleted")

    # ### end Alembic commands ###
