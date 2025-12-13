from flask import Flask, render_template, request, jsonify
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
        port=os.getenv("MYSQLPORT", 3306)
    )

# ---------------- ROUTES ---------------- #

@app.route('/login-page')
def login_page():
    return render_template('index.html')  # templates/login.html

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')  # templates/dashboard.html

# ---------------- Login API ---------------- #
@app.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Example query for login validation
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        # Return dummy token (replace with JWT in production)
        return jsonify({
            "token": "dummy-jwt-token",
            "user_id": user["id"],
            "user_name": user["name"],
            "role": user["role"]
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ---------------- Main ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

