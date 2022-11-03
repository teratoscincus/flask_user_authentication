from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

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
            try:
                # Make sure password is hashed successfully.
                password_hash = generate_password_hash(password)

                # Try to insert row into bd table, fails if username already exists.
                db.cursor.execute(
                    f"""
                    INSERT INTO users (username, password)
                    VALUES ('{username}', '{password_hash}')
                    """
                )
                # Make sure changes are committed.
                db.connection.commit()
            except:
                flash(f"User {username} is already registered.")
                # Rerender registration form if given username is taken.
                return render_template("register.html")
            else:
                # Redirect to homepage if registration was successful.
                return redirect(url_for("views.index"))
