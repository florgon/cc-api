"""
    Tests for utils views.
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
from flask import url_for


def test_read_utils_get_server_time(app, client):
    """
    Test for `utils/getServerTime` method of the API.
    """
    with app.test_request_context():
        response = client.get(url_for("utils.get_server_time"))

    assert response.status_code == 200
    assert "v" in response.json
    assert "success" in response.json
    assert "server_time" in response.json["success"]
