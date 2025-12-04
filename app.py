from flask import Flask, render_template, request, redirect, jsonify, session
import bcrypt
import sqlite3
import os


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect('vault.db')

    conn.row_factory = sqlite3.Row

    return conn


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")


@app.route('/')
def home():
    if not session.get("authenticated"):
        return redirect("/login")
    conn = get_db()
    passwords = conn.execute("SELECT * FROM passwords").fetchall()
    conn.close()
    return render_template("home.html", passwords=passwords)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        entered = request.form.get("password")
        if not entered:
            return "Password is required", 400

        entered = entered.encode()
        stored_hash = os.getenv("MASTER_HASH").encode()

        if bcrypt.checkpw(entered, stored_hash):
            session["authenticated"] = True
            return redirect("/")
        else:
            return "Wrong password", 403

    return render_template("login.html")


@app.route('/add', methods=['POST'])
def add():
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


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM passwords WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route('/get/<int:id>/<site>')
def get_by_id(id, site):
    conn = get_db()
    result = conn.execute("SELECT username, password FROM passwords WHERE id = ? AND site = ?", (id, site)).fetchone()
    conn.close()
    return jsonify({
        "username": result["username"],
        "password": result["password"]
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
