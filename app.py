from flask import Flask, request, render_template, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "tajne_heslo_123"  # môžeš zmeniť

DB_NAME = "cars.db"
APP_PASSWORD = "mojeheslo"  # 👈 SEM SI DAJ VLASTNÉ HESLO

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spz TEXT UNIQUE,
            name TEXT,
            oil_type TEXT,
            oil_amount REAL,
            oil_norm TEXT,
            oil_filter TEXT,
            air_filter TEXT,
            fuel_filter TEXT
        )
    """)
    db.commit()
    db.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == APP_PASSWORD:
            session["logged_in"] = True
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect("/login")

    car = None
    if request.method == "POST":
        spz = request.form["spz"]
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM cars WHERE spz = ?", (spz,))
        car = cur.fetchone()
        db.close()

    return render_template("index.html", car=car)

@app.route("/add", methods=["POST"])
def add_car():
    if not session.get("logged_in"):
        return redirect("/login")

    data = request.form
    db = get_db()
    db.execute("""
        INSERT INTO cars 
        (spz, name, oil_type, oil_amount, oil_norm, oil_filter, air_filter, fuel_filter)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["spz"], data["name"], data["oil_type"], data["oil_amount"],
        data["oil_norm"], data["oil_filter"], data["air_filter"], data["fuel_filter"]
    ))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/update", methods=["POST"])
def update_car():
    if not session.get("logged_in"):
        return redirect("/login")

    data = request.form
    db = get_db()
    db.execute("""
        UPDATE cars SET
            name=?, oil_type=?, oil_amount=?, oil_norm=?,
            oil_filter=?, air_filter=?, fuel_filter=?
        WHERE spz=?
    """, (
        data["name"], data["oil_type"], data["oil_amount"], data["oil_norm"],
        data["oil_filter"], data["air_filter"], data["fuel_filter"], data["spz"]
    ))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/delete/<spz>")
def delete_car(spz):
    if not session.get("logged_in"):
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM cars WHERE spz=?", (spz,))
    db.commit()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
