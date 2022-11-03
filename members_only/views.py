from time import sleep

from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError, OperationalError

from .database.database import Database
from .config import DATABASE_PATH

view = Blueprint("views", __name__)


@view.route("/")
def index():
    return render_template("index.html")


@view.route("/register", methods=("GET", "POST"))
def register():
    if request.method != "POST":
        # Render registration template for all methods except "POST".
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        db = Database(DATABASE_PATH)

        # Check that all fields have been filled.
        if not username:
            flash("Username is required.")
        elif not password:
            flash("Password is required.")
        else:
            # Hash password before writing to database.
            password_hash = generate_password_hash(password)
            try:
                # Try to insert row into bd table, fails if username already exists.
                db.cursor.execute(
                    f"""
                    INSERT INTO users (username, password)
                    VALUES ('{username}', '{password_hash}')
                    """
                )
                # Make sure changes are committed.
                db.connection.commit()
            except IntegrityError:
                # Given username is taken.
                flash(f"'{username}' is already registered.")
            except OperationalError:
                # Try committing again after 1 second.
                sleep(1)
                db.connection.commit()
            else:
                # Redirect to homepage if registration was successful.
                return redirect(url_for("views.index"))

        # Rerender registration template is something went wrong.
        return render_template("register.html")
