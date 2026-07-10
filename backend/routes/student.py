from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import cache
import os
from database import db
from datetime import datetime
from werkzeug.utils import secure_filename

from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application

stu_bp = Blueprint("student", __name__)

@stu_bp.route("/student/dashboard")
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
        "graduation_year": student.graduation_year,
        "skills": student.skills,
        "education": student.education,
        "experience": student.experience,
        "resume": student.resume
    })

@stu_bp.route("/student/update-profile", methods=["PUT"])
@jwt_required()
def update_student_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    data = request.json

    student.full_name = data.get(
        "full_name",
        student.full_name
    )

    student.department = data.get(
        "department",
        student.department
    )

    student.cgpa = data.get(
        "cgpa",
        student.cgpa
    )

    student.graduation_year = data.get(
        "graduation_year",
        student.graduation_year
    )

    student.skills = data.get(
        "skills",
        student.skills
    )

    student.education = data.get(
        "education",
        student.education
    )

    student.experience = data.get(
        "experience",
        student.experience
    )

    student.resume = data.get(
        "resume",
        student.resume
    )

    db.session.commit()
    cache.clear()
    return jsonify({
        "message": "Profile updated successfully"
    })

@stu_bp.route("/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "student":

        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    job = JobPosition.query.get(job_id)
    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    if job.status != "approved":
        return jsonify({
            "message": "Job not open for applications"
        }), 400

    existing_application = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if existing_application:
        return jsonify({
            "message": "Already applied"
        }), 400

    if job.eligible_department:
        eligible_departments = [
            dept.strip().upper()
            for dept in job.eligible_department.split(",")
        ]

        student_department = (
            student.department.strip().upper()
        )

        if student_department not in eligible_departments:
            return jsonify({
                "message": "Department not eligible"
            }), 400

    if job.eligible_batch:
        eligible_batches = [
            batch.strip()
            for batch in job.eligible_batch.split(",")
        ]

        student_batch = str(
            student.graduation_year
        ).strip()

        if student_batch not in eligible_batches:
            return jsonify({
                "message": "Graduation year not eligible"
            }), 400
        
    if (
        job.minimum_cgpa is not None and
        float(student.cgpa) < float(job.minimum_cgpa)):
        return jsonify({
            "message": "Required CGPA not met"
        }), 400

    if job.application_deadline:
        deadline = datetime.strptime(
            job.application_deadline,
            "%Y-%m-%d"
        ).date()
        today = datetime.today().date()

        if today > deadline:
            return jsonify({
                "message": "Application deadline has passed"
            }), 400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="applied" )

    db.session.add(application)
    db.session.commit()
    cache.clear()
    return jsonify({
        "message": "Application submitted successfully"
    })

@stu_bp.route("/student/jobs")
@jwt_required()
def approved_jobs():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id).first()

    jobs = JobPosition.query.filter(
        JobPosition.status.in_(["approved", "closed"])).all()

    result = []

    for job in jobs:
        company = Company.query.get(job.company_id)

        existing_application = Application.query.filter_by(
            student_id=student.id,
            job_id=job.id).first()

        is_eligible = True
        eligibility_message = ""
        if job.eligible_department:
            eligible_departments = [
                dept.strip().upper()
                for dept in job.eligible_department.split(",")
            ]

            student_department = student.department.strip().upper()
            if student_department not in eligible_departments:
                is_eligible = False
                eligibility_message = "Department not eligible"

        if is_eligible and job.eligible_batch:
            eligible_batches = [
                batch.strip()
                for batch in job.eligible_batch.split(",")
            ]
            student_batch = str(student.graduation_year).strip()

            if student_batch not in eligible_batches:
                is_eligible = False
                eligibility_message = "Graduation year not eligible"

        if (is_eligible and
            job.minimum_cgpa is not None and
            float(student.cgpa) < float(job.minimum_cgpa)):
            is_eligible = False
            eligibility_message = "Required CGPA not met"

        if is_eligible and job.application_deadline:
            deadline = datetime.strptime(job.application_deadline,
                "%Y-%m-%d").date()

            today = datetime.today().date()

            if today > deadline:
                is_eligible = False
                eligibility_message = "Application deadline has passed"

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name if company else "Unknown",
            "location": job.location,
            "salary": job.salary,
            "description": job.description,
            "status": job.status,
            "applied": bool(existing_application),
            "application_status": existing_application.status if existing_application else "",
            "is_eligible": is_eligible,
            "eligibility_message": eligibility_message})

    return jsonify(result)


@stu_bp.route("/student/my-applications")
@jwt_required()
def my_applications():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    result = []

    for application in applications:
        job = JobPosition.query.get(
            application.job_id
        )

        company = Company.query.get(
            job.company_id
        )

        result.append({
            "job_title": job.title,
            "company_name": company.company_name,
            "status": application.status,
            "interview_date": (
                application.interview_date
                if application.interview_date
                else "Not Scheduled"
            ),
            "feedback": (
                application.feedback
                if application.feedback
                else "No Feedback Yet")})

    return jsonify(result)

@stu_bp.route("/student/export-csv")
@jwt_required()
def export_csv():
    from tasks import export_student_csv
    
    user_id = get_jwt_identity()
    user = User.query.get(
        int(user_id)
    )
    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    task = export_student_csv.delay(
        student.id
    )
    filename = f"student_{student.id}.csv"

    return jsonify({
        "message": "CSV export started successfully",
        "task_id": task.id,
        "file_url": f"http://127.0.0.1:5000/exports/{filename}"})

@stu_bp.route("/student/check-export")
@jwt_required()
def check_export():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    filename = f"student_{student.id}.csv"
    filepath = os.path.join(
        "exports",
        filename
    )

    if os.path.exists(filepath):
        return jsonify({
            "exists": True,
            "filename": filename})

    return jsonify({
        "exists": False
    })

@stu_bp.route("/student/upload-resume", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if "resume" not in request.files:
        return jsonify({
            "message": "No resume uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "No file selected"
        }), 400

    filename = secure_filename(file.filename)

    upload_path = os.path.join(
        "uploads",
        filename)

    file.save(upload_path)

    student.resume = filename

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume": filename})