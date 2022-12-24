"""
    Tests for utils views.
"""
from flask import url_for

def test_read_utils_get_server_time(app, client):
    with app.test_request_context():
        response = client.get(url_for("utils.get_server_time"))

    assert response.status_code == 200
    assert "v" in response.json
    assert "success" in response.json
    assert "server_time" in response.json["success"]
