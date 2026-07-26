from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db
from extensions import jwt, cache
from flask import send_from_directory
from models.user import User

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.student import stu_bp
from routes.company import cmp_bp

app = Flask(__name__)

app.config.from_object(Config)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["JWT_SECRET_KEY"] = "placement-secret-key"

db.init_app(app)

jwt.init_app(app)

cache.init_app(app)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(stu_bp)
app.register_blueprint(cmp_bp)


with app.app_context():
    db.create_all()
    admin_exists = User.query.filter_by(
        role="admin"
    ).first()
    if not admin_exists:
        admin = User(
            email="admin@ppa.com",
            password="admin123",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename)

@app.route("/")
def home():
    return jsonify({"message": "Placement Portal API Running"})

@app.route("/exports/<filename>")
def download_export(filename):
    return send_from_directory(
        "exports",
        filename
    )

@app.route("/reports/<filename>")
def view_report(filename):
    return send_from_directory(
        "reports",filename)

if __name__ == "__main__":
    app.run(debug=True)