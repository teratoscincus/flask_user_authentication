from time import sleep

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
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
        given_username = request.form["username"]
        given_password = request.form["password"]

        db = Database(DATABASE_PATH)

        # Check that all fields have been filled.
        if not given_username:
            flash("Username is required.")
        elif not given_password:
            flash("Password is required.")
        else:
            # Hash password before writing to database.
            password_hash = generate_password_hash(given_password)
            try:
                # Try to insert row into bd table, fails if username already exists.
                db.cursor.execute(
                    f"""
                    INSERT INTO users (username, password)
                    VALUES ('{given_username}', '{password_hash}')
                    """
                )
                # Make sure changes are committed.
                db.connection.commit()
            except IntegrityError:
                # Given username is taken.
                flash(f"'{given_username}' is already registered.")
            except OperationalError:
                # Try committing again after 1 second.
                sleep(1)
                db.connection.commit()
            else:
                # Redirect to homepage if registration was successful.
                return redirect(url_for("views.index"))

        # Rerender registration template is something went wrong.
        return render_template("register.html")


@view.route("/login", methods=("GET", "POST"))
def login():
    if request.method != "POST":
        # Render login template for all methods except "POST".
        return render_template("login.html")
    else:
        given_username = request.form["username"]
        given_password = request.form["password"]

        db = Database(DATABASE_PATH)

        # Check that all fields have been filled.
        if not given_username:
            flash("Username is required.")
        elif not given_password:
            flash("Password is required.")
        else:
            # Check for match in database.
            user = db.cursor.execute(
                f"""
                SELECT * FROM users 
                WHERE username = '{given_username}'
                """
            ).fetchone()

            # Check that username is registered.
            if user is None:
                flash("Incorrect username.")
            else:
                # Unpack tuple returned from SQL query.
                user_id = user[0]
                user_username = user[1]
                user_password = user[2]

                # Check that the password matches.
                if not check_password_hash(user_password, given_password):
                    flash("Incorrect password.")
                else:
                    # Login successful
                    session.clear()
                    session["user_id"] = user_id
                    session["username"] = user_username

                    return redirect(url_for("views.index"))

        # Login not successful - rerender template.
        return render_template("login.html")


@view.route("/log_out")
def log_out():
    """Clear session and redirect to index page."""
    session.clear()
    flash("You have been logged out")

    return redirect(url_for("views.index"))
