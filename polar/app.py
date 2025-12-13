import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration (Railway ENV variables)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://"
    f"{os.environ['DB_USER']}:"
    f"{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:"
    f"{os.environ['DB_PORT']}/"
    f"{os.environ['DB_NAME']}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(15), nullable=False)

with app.app_context():
    db.create_all()

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/customers")
def customers():
    return render_template("customers.html")

# API
@app.route("/add_customer", methods=["POST"])
def add_customer():
    data = request.get_json()
    customer = Customer(
        company_name=data["company_name"],
        contact_phone=data["contact_phone"]
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Customer added successfully"})
