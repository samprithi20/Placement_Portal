from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import cache,jwt

from database import db

from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
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

    pending_jobs = JobPosition.query.filter_by(
        status="pending"
    ).count()

    total_applications = Application.query.count()

    return jsonify({
    "total_students": total_students,
    "total_companies": total_companies,
    "total_jobs": total_jobs,
    "total_applications": total_applications,
    "pending_companies": pending_companies,
    "pending_jobs": pending_jobs
    })


@admin_bp.route("/admin/pending-jobs")
@jwt_required()
def pending_jobs():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    jobs = JobPosition.query.filter_by(
        status="pending"
    ).all()

    result = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name,
            "location": job.location,
            "salary": job.salary,
            "status": job.status
        })

    return jsonify(result)

@admin_bp.route("/admin/approve-job/<int:job_id>", methods=["PUT"])
@jwt_required()
def approve_job(job_id):

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    job.status = "approved"

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Job approved successfully"
    })

@admin_bp.route("/admin/reject-job/<int:job_id>", methods=["DELETE"])
@jwt_required()
def reject_job(job_id):

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    db.session.delete(job)

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Job removed successfully"
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

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name,
            "location": job.location,
            "salary": job.salary,
            "status": job.status
        })

    return jsonify(result)

@admin_bp.route("/admin/search-jobs")
@jwt_required()
def search_jobs():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    query = request.args.get("query")

    jobs = JobPosition.query.filter(
        JobPosition.title.ilike(f"%{query}%")
    ).all()

    result = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name,
            "location": job.location,
            "salary": job.salary,
            "status": job.status
        })

    return jsonify(result)

@admin_bp.route("/admin/applications")
@jwt_required()
def all_applications():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    applications = Application.query.all()

    result = []

    for application in applications:

        result.append({
            "id": application.id,
            "student_id": application.student_id,
            "job_id": application.job_id,
            "status": application.status
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
        "message": "Company approved successfully"
    })

@admin_bp.route("/admin/reject-company/<int:company_id>", methods=["DELETE"])
@jwt_required()
def reject_company(company_id):

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

    db.session.delete(company)

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Company removed successfully"
    })

@admin_bp.route("/admin/pending-companies")
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
            "hr_name": company.hr_name,
            "hr_email":company.hr_email
        })

    return jsonify(result)

@admin_bp.route("/admin/companies")
@jwt_required()
@cache.cached(timeout=300)
def all_companies():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    companies = Company.query.all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "approval_status": company.approval_status,
            "location": company.location
        })

    return jsonify(result)

@admin_bp.route("/admin/search-companies")
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def search_companies():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    query = request.args.get("query")

    companies = Company.query.filter(
    (Company.company_name.ilike(f"%{query}%")) |
    (Company.industry.ilike(f"%{query}%"))
    ).all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "approval_status": company.approval_status
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

    students = Student.query.all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "full_name": student.full_name,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year
        })

    return jsonify(result)

@admin_bp.route("/admin/search-students")
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def search_students():

    user_id = get_jwt_identity()

    admin = User.query.get(int(user_id))

    if admin.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    query = request.args.get("query")

    students = Student.query.filter(
    (Student.full_name.ilike(f"%{query}%")) |
    (Student.id.like(f"%{query}%"))
    ).all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "full_name": student.full_name,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year
        })

    return jsonify(result)

@admin_bp.route("/admin/deactivate-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def deactivate_user(user_id):

    current_user = User.query.get(
        int(get_jwt_identity())
    )

    if current_user.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_active = False

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "User deactivated"
    })

@admin_bp.route("/admin/blacklist-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_user(user_id):

    current_user = User.query.get(
        int(get_jwt_identity())
    )

    if current_user.role != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_blacklisted = True

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "User blacklisted successfully"
    })

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    output = []

    for student in students:

        output.append({
            "id": student.id,
            "full_name": student.full_name,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year
        })

    return jsonify(output)

@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def get_companies():

    companies = Company.query.all()

    output = []

    for company in companies:

        output.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "approval_status": company.approval_status
        })

    return jsonify(output)

@admin_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():

    jobs = JobPosition.query.all()

    output = []

    for job in jobs:

        output.append({
            "id": job.id,
            "title": job.title,
            "salary": job.salary,
            "company_name": job.company.company_name
        })

    return jsonify(output)
