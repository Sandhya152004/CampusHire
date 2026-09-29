from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from cache import cache
from dotenv import load_dotenv
load_dotenv()

import os
from flask import send_from_directory

from config import Config
from models import db
from routes.auth import auth_bp
from models.user import User
from werkzeug.security import generate_password_hash

from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp

from mail import mail

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

    admin_email = os.getenv(
        "ADMIN_EMAIL",
        "admin@placement.com"
    )

    admin_password = os.getenv(
        "ADMIN_PASSWORD",
        "admin123"
    )

    admin = User.query.filter_by(
        email=admin_email
    ).first()

    if not admin:
        admin_user = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            role="admin"
        )

        db.session.add(admin_user)
        db.session.commit()

mail.init_app(app)

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads",
    "resumes"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "placementportaljwtsecret"
)
jwt = JWTManager(app)

cache.init_app(
    app,
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_URL": os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0"
        ),
        "CACHE_DEFAULT_TIMEOUT": 300
    })


@app.route("/")
def home():
    return {
        "message": "Backend Connected Successfully"
    }
    
@app.route('/uploads/resumes/<filename>')
def uploaded_resume(filename):

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename

    )

if __name__ == "__main__":
    app.run(debug=True)
    
