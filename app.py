from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True  # set True in HTTPS
)


# ---------------- MySQL Connection ----------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=int(os.getenv("MYSQLPORT", 3306))
        )
        return conn
    except Exception as e:
        print("DB Connection Error:", e)
        return None

# ==================================================
# LOGIN REQUIRED DECORATOR
# ==================================================
def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_email" not in session:
            if request.accept_mimetypes.accept_html:
                return redirect(url_for("login_page"))
            return jsonify({"error": "Authentication required"}), 401
        return view_func(*args, **kwargs)
    return wrapped

# ---------------- ROUTES ----------------
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))
    
@app.route("/customer")
@login_required
def customer():
    return render_template("customer.html")

# ---------------- LOGIN API ----------------
@app.route("/api/login", methods=["POST"])
def login_api():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    if conn is None:
        return jsonify({"success": False, "error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT name FROM users WHERE name=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session["user_email"] = user["name"]
        session["logged_in"] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401
        

# ---------------- Instruments ----------------
@app.route("/api/instruments")
def api_instruments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM instruments WHERE status='Active'")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# ---------------- Services ----------------
@app.route("/api/services")
def api_services():
    status = request.args.get("status", None)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if status:
        cursor.execute("SELECT s.service_id, s.service_type, s.service_date, s.status, i.instrument_name, c.customer_name FROM services s JOIN instruments i ON s.instrument_id=i.instrument_id JOIN customers c ON s.customer_id=c.customer_id WHERE s.status=%s ORDER BY s.service_date DESC", (status,))
    else:
        cursor.execute("SELECT s.service_id, s.service_type, s.service_date, s.status, i.instrument_name, c.customer_name FROM services s JOIN instruments i ON s.instrument_id=i.instrument_id JOIN customers c ON s.customer_id=c.customer_id ORDER BY s.service_date DESC")
    
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# ==================================================
# DASHBOARD APIs
# ==================================================

@app.route("/api/dashboard/stats")
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(company_id) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM instruments")
    instruments = cursor.fetchone()[0]

    p="not done"
    cursor.execute("SELECT COUNT(*) FROM service_records WHERE status = %s ",(p,))
    pending_services = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "customers": customers,
        "instruments": instruments,
        "pending_services": pending_services,
        "critical":0
    })


# ---------------- RECENT CUSTOMERS ----------------
@app.route("/api/customers/recent")
@login_required
def recent_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT company_id, company_name, company_type,
               conatct_name, contact_phone
        FROM customers
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)


# ---------------- Customers ----------------
@app.route("/api/customers")
@login_required
def api_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers ORDER BY company_id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# ---------------- ADD CUSTOMERS ----------------
@app.route("/api/add_customers", methods=["POST"])
@login_required
def add_customers():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON received"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers
        ( company_id, company_name, company_type, conatct_name, cantact_mail, contact_phone)
        VALUES (%s,%s, %s, %s, %s, %s)
    """, (
        data["cid"],
        data["cname"],
        data["ctype"],
        data["ccname"],
        data["cmail"],
        data["cphone"]
       ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer added successfully"})

# ---------------- UPDATE CUSTOMERS ----------------
@app.route("/api/update_customers", methods=["POST"])
@login_required
def update_customers():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON received"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE customers
    SET
        company_name = %s,
        company_type = %s,
        conatct_name = %s,
        cantact_mail = %s,
        contact_phone = %s
    WHERE customer_id = %s
""", (
    data["company_name"],
    data["company_type"],
    data["contact_name"],
    data["contact_mail"],
    data["contact_phone"],
    data["company_id"]
))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer updated successfully"})
    
# ---------------- INSTRUMENTS BY CUSTOMER ----------------
@app.route("/api/instruments/<int:company_id>")
def get_instruments(company_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM instruments
        WHERE company_id = %s
    """, (company_id,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)


# ---------------- PENDING SERVICES ----------------
@app.route("/api/services/pending")
def pending_services():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        s.i_serial,
        i.company_name,
        i.m_no,
        i.i_type,
        s.status,
        s.problem_reported
    FROM service_records s
    JOIN instruments i 
        ON s.i_serial = i.i_serial
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=False)


