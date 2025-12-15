from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ---------------- MySQL Connection ----------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT",3306))
    )

# ---------------- ROUTES ----------------
@app.route("/")
def login_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- LOGIN HANDLER ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT name FROM users WHERE name=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    
    if user:
        return jsonify({
            "success": True,
            "email": user["email"]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=flase)








