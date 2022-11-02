"""Configurations fo the app."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path().parent.resolve()
APP_DIR = ROOT_DIR / "members_only"

# Environmental variables
DOTENV_PATH = APP_DIR / ".env"
load_dotenv(DOTENV_PATH)

# Development config
FLASK_ENV = "development"
DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")

# Development database
DB_DIR = APP_DIR / "database"
DATABASE = "db.sqlite3"
DATABASE_PATH = DB_DIR / DATABASE
SCHEMA_PATH = DB_DIR / "schema.sql"
