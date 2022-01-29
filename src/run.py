#!usr/bin/python
"""
    URL shortener application runner.
    Runs the Flask application.
"""

import app

if __name__ == "__main__":
    app.create().run(debug=True, port=80)
