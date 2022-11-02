"""Configurations fo the app."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Environmental variables
DOTENV_PATH = Path().parent.resolve() / ".env"
load_dotenv(DOTENV_PATH)

# Development config
FLASK_ENV = "development"
DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")
