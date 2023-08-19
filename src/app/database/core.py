"""
    Database core sessions / sessionmakers and migrations.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask


def init_with_app(app: Flask) -> None:
    """
    Initializes database requirements with Flask app by connecting ORM and running migrations if required.
    """
    db.init_app(app)
    migrate.init_app(app, db)


db = SQLAlchemy()
migrate = Migrate()
