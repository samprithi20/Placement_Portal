from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_cors import CORS
from config import Config
from database import db

from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

app = Flask(__name__)

app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = "placement-secret-key"

db.init_app(app)

jwt = JWTManager(app)

CORS(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({
        "message": "Placement Portal API Running"
    })


@app.route("/register/student", methods=["POST"])
def register_student():
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
        role="student"
    )
    db.session.add(user)
    db.session.commit()
    student = Student(
        user_id=user.id,
        full_name=data["full_name"],
        department=data.get("department"),
        cgpa=data.get("cgpa"),
        graduation_year=data.get("graduation_year"),
        skills=data.get("skills")
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({
        "message": "Student registered successfully"
    })

@app.route("/register/company", methods=["POST"])
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

    return jsonify({
        "message": "Company registered. Waiting for admin approval."
    })


@app.route("/login", methods=["POST"])
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

    if user.role == "company":
        company = Company.query.filter_by(
            user_id=user.id
        ).first()

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

@app.route("/admin/dashboard")
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    total_students = User.query.filter_by(
        role="student"
    ).count()

    total_companies = User.query.filter_by(
        role="company"
    ).count()

    total_jobs = JobPosition.query.count()

    pending_companies = Company.query.filter_by(
        approval_status="pending"
    ).count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "pending_companies": pending_companies
    })


@app.route("/student/dashboard")
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    return jsonify({
        "full_name": student.full_name,
        "department": student.department,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year
    })


@app.route("/company/dashboard")
@jwt_required()
def company_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "approval_status": company.approval_status
    })


@app.route("/admin/approve-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):
    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully"
    })

@app.route("/admin/pending-companies")
@jwt_required()
def pending_companies():
    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    companies = Company.query.filter_by(
        approval_status="pending"
    ).all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "hr_name": company.hr_name
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)