from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import cache
from database import db
from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

cmp_bp = Blueprint("company", __name__)

@cmp_bp.route("/company/dashboard")
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

    total_jobs = JobPosition.query.filter_by(
        company_id=company.id
    ).count()

    jobs = JobPosition.query.filter_by(
        company_id=company.id
    ).all()

    job_ids = [job.id for job in jobs]

    total_applications = Application.query.filter(
        Application.job_id.in_(job_ids)
    ).count()

    total_placed = Application.query.filter(
        Application.job_id.in_(job_ids),
        Application.status == "placed"
    ).count()

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "approval_status": company.approval_status,
        "location": company.location,
        "hr_name": company.hr_name,
        "website": company.website,
        "hr_email": company.hr_email,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_placed": total_placed })

@cmp_bp.route("/company/update-profile", methods=["PUT"])
@jwt_required()
def update_company_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    data = request.json

    company.company_name = data.get(
        "company_name",
        company.company_name
    )

    company.industry = data.get(
        "industry",
        company.industry
    )

    company.location = data.get(
        "location",
        company.location
    )

    company.hr_name = data.get(
        "hr_name",
        company.hr_name
    )

    company.website = data.get(
        "website",
        company.website
    )

    company.hr_email = data.get(
        "hr_email",
        company.hr_email
    )

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Company profile updated successfully"})

@cmp_bp.route("/company/create-job", methods=["POST"])
@jwt_required()
def create_job():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    if company.approval_status != "approved":
        return jsonify({
            "message": "Company not approved"
        }), 403

    data = request.json

    job = JobPosition(
    company_id=company.id,
    title=data["title"],
    description=data["description"],
    location=data["location"],
    salary=data["salary"],
    required_skills=data.get("required_skills"),
    experience_required=data.get("experience_required"),
    benefits=data.get("benefits"),
    status="pending",
    eligible_department=data.get("eligible_department"),
    minimum_cgpa=data.get("minimum_cgpa"),
    eligible_batch=data.get("eligible_batch"),
    application_deadline=data.get("application_deadline") )

    db.session.add(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Job created and waiting for admin approval"
    })


@cmp_bp.route("/company/jobs")
@jwt_required()
def company_jobs():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    jobs = JobPosition.query.filter_by(
        company_id=company.id
    ).all()

    result = []

    for job in jobs:
        application_count = Application.query.filter_by(
            job_id=job.id
        ).count()

        result.append({
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "salary": job.salary,
            "status": job.status,
            "applications": application_count,
            "application_deadline": job.application_deadline
        })

    return jsonify(result)

@cmp_bp.route("/company/job-applications/<int:job_id>")
@jwt_required()
def job_applications(job_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    applications = Application.query.filter_by(
        job_id=job_id
    ).all()

    job = JobPosition.query.get(job_id)

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    if job.company_id != company.id:
        return jsonify({
            "message": "Unauthorized access"
        }), 403
    result = []

    for application in applications:
        student = Student.query.get(
            application.student_id
        )

        result.append({
            "application_id": application.id,
            "student_name": student.full_name,
            "department": student.department,
            "cgpa": student.cgpa,
            "status": application.status,
            "interview_date": application.interview_date,
            "resume": (
                f"http://127.0.0.1:5000/uploads/{student.resume}"
                if student.resume else None
            ),
            "feedback": application.feedback
        })

    return jsonify(result)

@cmp_bp.route("/company/applications")
@jwt_required()
def company_applications():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({"message": "Unauthorized"}), 403

    company = Company.query.filter_by(user_id=user.id).first()

    jobs = JobPosition.query.filter_by(company_id=company.id).all()
    job_ids = [job.id for job in jobs]

    applications = Application.query.filter(
        Application.job_id.in_(job_ids)
    ).all()

    result = []

    for app in applications:
        student = Student.query.get(app.student_id)
        job = JobPosition.query.get(app.job_id)

        result.append({
            "id": app.id,
            "student_name": student.full_name,
            "job_title": job.title,
            "status": app.status,
            "resume": (
                f"http://127.0.0.1:5000/uploads/{student.resume}"
                if student.resume else None
            )
        })

    return jsonify(result)

@cmp_bp.route("/company/update-application/<int:application_id>", methods=["PUT"])
@jwt_required()
def update_application(application_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    data = request.json

    allowed_statuses = [
        "applied",
        "interview scheduled",
        "rejected",
        "placed"
    ]

    if data["status"] not in allowed_statuses:
        return jsonify({
            "message": "Invalid status"
        }), 400

    application.status = data["status"]
    application.feedback = data.get("feedback")

    if data["status"] == "placed":
        job = JobPosition.query.get(application.job_id)
        existing_placement = Placement.query.filter_by(
            student_id=application.student_id,
            company_id=job.company_id).first()

        if not existing_placement:
            placement = Placement(
                student_id=application.student_id,
                company_id=job.company_id,
                position=job.title,
                salary=job.salary
            )
            db.session.add(placement)

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Application updated successfully"
    })

@cmp_bp.route("/company/schedule-interview/<int:application_id>", methods=["PUT"])
@jwt_required()
def schedule_interview(application_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    application = Application.query.get(
        application_id
    )

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    data = request.json

    application.interview_date = data["interview_date"]
    application.status = "interview scheduled"
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Interview scheduled",
        "status" : application.status
    })

@cmp_bp.route("/company/close-job/<int:job_id>", methods=["PUT"])
@jwt_required()
def close_job(job_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    job.status = "closed"
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Job closed successfully"})