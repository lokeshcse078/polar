from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Railway MySQL environment variables
    DB_USER = os.getenv("MYSQLUSER")
    DB_PASSWORD = os.getenv("MYSQLPASSWORD")
    DB_HOST = os.getenv("MYSQLHOST")
    DB_PORT = os.getenv("MYSQLPORT")
    DB_NAME = os.getenv("MYSQLDATABASE")

    # IMPORTANT: mysql+mysqlconnector
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ---------------- ROUTES ---------------- #

    @app.route('/login-page')
    def login_page():
        return render_template('login.html')  # make sure file is in templates/

    # ---------------- Dashboard Page ----------------
    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')  # must exist in templates/



app = create_app()

if __name__ == "__main__":
    app.run()

