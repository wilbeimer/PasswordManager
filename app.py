from flask import Flask, render_template, request, redirect, jsonify, session
import bcrypt
import sqlite3
import os
from datetime import timedelta
from flask_cors import CORS
from generator import generate_password


def get_db() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database.
    Sets row_factory to sqlite3.Row for easy column-name access (result['column_name']).
    """
    conn = sqlite3.connect('vault.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
# Load the secret key for session management from environment variables.
# The 'dev_secret' fallback should only be used during local development.
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
app.permanent_session_lifetime = timedelta(minutes=1)

# to talk to this local server, preventing 403 Forbidden errors.
CORS(app)


@app.route('/status')
def status():
    """Simple API health check endpoint for the content script."""
    return jsonify({'status': 'ok'})


@app.route('/')
def home():
    """The main dashboard view for the web interface."""
    # Enforce authentication: if the user isn't logged in, redirect them.
    if not session.get("authenticated"):
        return redirect("/login")

    conn = get_db()
    # Fetch all passwords to display in the table on the dashboard
    passwords = conn.execute("SELECT * FROM passwords").fetchall()
    conn.close()
    return render_template("home.html", passwords=passwords)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles both displaying the login form and processing the master password."""
    if request.method == "POST":
        entered = request.form.get("password")
        if not entered:
            return "Password is required", 400

        entered = entered.encode()
        # Retrieve the master hash from environment variables for comparison.
        stored_hash = os.getenv("MASTER_HASH", "").encode()

        if not stored_hash:
            # Important: Bail out if the configuration is incomplete.
            return "Configuration Error: MASTER_HASH not set in environment.", 500

        # Securely compare the entered password with the stored hash.
        if bcrypt.checkpw(entered, stored_hash):
            session.permanent = True
            session["authenticated"] = True
            return redirect("/")
        else:
            return "Wrong password", 403 # 403 Forbidden is often used for authorization failures

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clears the session and redirects the user back to the login page."""
    session.clear()
    return redirect("/login")


@app.route('/add', methods=['POST'])
def add():
    """Adds a new password entry submitted via the web form."""
    # Data modifying routes should always be protected.
    if not session.get("authenticated"):
        return "Unauthorized", 401

    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    conn.execute(
        "INSERT INTO passwords (site, username, password) VALUES (?,?,?)",
        (site, username, password)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    length_str = request.values.get('length')

    if length_str is None or not length_str.isdigit():
        # Returns 400 if 'length' is missing or not a number, preventing a crash.
        return jsonify({"message": "Missing or invalid 'length' parameter."}), 400

    length = int(length_str)

    MIN_LENGTH = 8
    MAX_LENGTH = 50

    if length < MIN_LENGTH or length > MAX_LENGTH:
        return jsonify({"message": f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}."}), 400

    password = generate_password(length)

    return jsonify({
        "message": "Password generated successfully",
        "password": password
    }), 200


@app.route('/delete/<int:id>')
def delete(id):
    """Deletes a specific password entry by ID."""
    if not session.get("authenticated"):
        return "Unauthorized", 401

    conn = get_db()
    conn.execute("DELETE FROM passwords WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route('/get/<site>')
def get_by_site(site):
    """
    API endpoint to retrieve credentials for a site, used by the content script.
    Crucially, handles the case where the site is not found to prevent a 500 server crash.
    """
    conn = get_db()
    # Note: Use fetchone() as we only expect one match.
    result = conn.execute("SELECT username, password FROM passwords WHERE site = ?", (site,)).fetchone()
    conn.close()

    # Check if the query returned a result (i.e., not None).
    if result:
        # Success: Return the credentials as JSON with a 200 OK status.
        return jsonify({
            "username": result["username"],
            "password": result["password"]
        })
    else:
        return jsonify({"message": f"Credentials not found for site: {site}"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
