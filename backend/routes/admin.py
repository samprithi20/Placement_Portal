from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import cache
from database import db

import os
from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    total_students = User.query.filter_by(
        role="student",
        is_blacklisted=False).count()

    total_companies = User.query.filter_by(
        role="company",
        is_blacklisted=False).count()

    total_jobs = JobPosition.query.count()

    pending_companies = Company.query.filter_by(
        approval_status="pending").count()

    pending_jobs = JobPosition.query.filter_by(
        status="pending").count()

    total_applications = Application.query.count()

    return jsonify({
    "total_students": total_students,
    "total_companies": total_companies,
    "total_jobs": total_jobs,
    "total_applications": total_applications,
    "pending_companies": pending_companies,
    "pending_jobs": pending_jobs})


@admin_bp.route("/admin/pending-jobs")
@jwt_required()
def pending_jobs():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    jobs = JobPosition.query.filter_by(
        status="pending").all()

    result = []

    for job in jobs:
        company = Company.query.get(job.company_id)

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name,
            "location": job.location,
            "salary": job.salary,
            "status": job.status})

    return jsonify(result)

@admin_bp.route("/admin/approve-job/<int:job_id>", methods=["PUT"])
@jwt_required()
def approve_job(job_id):
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Job not found"}), 404

    job.status = "approved"
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Job approved successfully"})

@admin_bp.route("/admin/reject-company/<int:company_id>", methods=["DELETE"])
@jwt_required()
def reject_company(company_id):
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    user = User.query.get(company.user_id)

    db.session.delete(company)

    if user:
        db.session.delete(user)

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Company removed successfully"
    })

@admin_bp.route("/admin/reject-job/<int:job_id>", methods=["DELETE"])
@jwt_required()
def reject_job(job_id):
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Job rejected successfully"
    })

@admin_bp.route("/admin/jobs")
@jwt_required()
@cache.cached(timeout=300)
def all_jobs():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    jobs = JobPosition.query.all()

    result = []

    for job in jobs:
        company = Company.query.get(job.company_id)
        application_count = Application.query.filter_by(
            job_id=job.id).count()

        result.append({
            "id": job.id,
            "company_name": company.company_name if company else "Unknown",
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "status": job.status,
            "required_skills": job.required_skills,
            "experience_required": job.experience_required,
            "benefits": job.benefits,
            "eligible_department": job.eligible_department,
            "minimum_cgpa": job.minimum_cgpa,
            "eligible_batch": job.eligible_batch,
            "application_deadline": str(job.application_deadline) if job.application_deadline else None,
            "applications": application_count
        })

    return jsonify(result)


@admin_bp.route("/admin/approve-company/<int:company_id>", methods=["PUT"])
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
    cache.clear()

    return jsonify({
        "message": "Company approved successfully"})

@admin_bp.route("/admin/pending-companies")
@jwt_required()
def pending_companies():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))
    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"}), 403

    companies = Company.query.filter_by(
        approval_status="pending").all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "hr_name": company.hr_name,
            "hr_email":company.hr_email})

    return jsonify(result)

@admin_bp.route("/admin/companies")
@jwt_required()
@cache.cached(timeout=300)
def all_companies():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))
    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"}), 403

    companies = Company.query.join(
        User,
        Company.user_id == User.id
    ).filter(
        User.is_blacklisted == False).all()

    result = []

    for company in companies:
        user = User.query.get(company.user_id)

        result.append({
            "id": company.id,
            "user_id": user.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "approval_status": company.approval_status,
            "location": company.location,
            "is_active": user.is_active
        })

    return jsonify(result)

@admin_bp.route("/admin/students")
@jwt_required()
@cache.cached(timeout=300)
def all_students():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    students = Student.query.join(
        User,
        Student.user_id == User.id).filter(User.is_blacklisted == False).all()

    result = []

    for student in students:
        user = User.query.get(student.user_id)

        result.append({
            "id": student.id,
            "user_id": user.id,
            "full_name": student.full_name,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "resume": student.resume,
            "is_active": user.is_active
        })

    return jsonify(result)

@admin_bp.route("/admin/deactivate-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def deactivate_user(user_id):
    admin = User.query.get(int(get_jwt_identity()))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = not user.is_active 

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "User status updated",
        "is_active": user.is_active
    })

@admin_bp.route("/admin/blacklist-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_user(user_id):

    admin = User.query.get(int(get_jwt_identity()))

    if admin.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_blacklisted = True
    user.is_active = False  

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "User permanently blacklisted"
    })

@admin_bp.route("/admin/reports")
@jwt_required()
def get_reports():
    user_id = get_jwt_identity()
    admin = User.query.get(int(user_id))
    if not admin or admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403
    filename = "monthly_report.html"

    filepath = os.path.join(
        "reports", filename )

    if os.path.exists(filepath):
        return jsonify({
            "filename": filename,
            "url": f"http://127.0.0.1:5000/reports/{filename}"
        })

    return jsonify({
        "message": "No report available"
    }), 404

