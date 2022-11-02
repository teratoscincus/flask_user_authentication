"""Create the app instance and load configurations."""

import os

from flask import Flask

from members_only.views import view


def create_app():
    """Create, configure, and return the flask app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile("config.py")

    app.register_blueprint(view)

    return app
