"""Create the app instance."""

import os

from flask import Flask


def create_app():
    """Create and return the flask app."""
    app = Flask(__name__)

    return app
