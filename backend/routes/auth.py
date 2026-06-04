from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import cache

from werkzeug.utils import secure_filename
import os

from database import db

from models.user import User
from models.student import Student
from models.company import Company

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.form

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    user = User(
        email=data["email"],
        password=data["password"],
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    resume_filename = None

    if "resume" in request.files:

        file = request.files["resume"]

        if file.filename != "":

            filename = secure_filename(file.filename)

            upload_path = os.path.join(
                "uploads",
                filename
            )

            file.save(upload_path)

            resume_filename = filename

    student = Student(

        user_id=user.id,

        full_name=data["full_name"],

        department=data.get("department"),

        cgpa=data.get("cgpa"),

        graduation_year=data.get("graduation_year"),

        skills=data.get("skills"),

        education=data.get("education"),

        experience=data.get("experience"),

        resume=resume_filename

    )

    db.session.add(student)

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Student registered successfully"
    })



@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.json
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()
    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    user = User(
        email=data["email"],
        password=data["password"],
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    #cache.clear()

    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        industry=data.get("industry"),
        location=data.get("location"),
        website=data.get("website"),
        hr_name=data.get("hr_name"),
        hr_email=data.get("hr_email"),
        approval_status="pending"
    )

    db.session.add(company)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Company registered. Waiting for admin approval."
    })


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid credentials"
        }), 401
    
    if not user.is_active:
        return jsonify({
            "message": "Account deactivated"
        }), 403

    if user.is_blacklisted:
        return jsonify({
            "message": "User is blacklisted"
        }), 403

    if user.role == "company":
        company = Company.query.filter_by(
            user_id=user.id
        ).first()

        if not company:
            return jsonify({
                "message": "Company profile not found"
            }), 404

        if company.approval_status != "approved":
            return jsonify({
                "message": "Company not approved by admin"
            }), 403

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "token": access_token,
        "role": user.role,
        "message": "Login successful"
    })
