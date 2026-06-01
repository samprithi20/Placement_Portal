from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import cache,jwt
from werkzeug.utils import secure_filename
import os
from database import db

from models.user import User
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

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

    existing_application = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if existing_application:
        return jsonify({
            "message": "Already applied"
        }), 400
    
    if student.cgpa < job.min_cgpa:
        return jsonify({
            "message": "Not eligible due to CGPA"
        }), 400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="applied"
    )

    db.session.add(application)

    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully"
    })

@stu_bp.route("/student/jobs")
@jwt_required()
@cache.cached(timeout=300)
def approved_jobs():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    jobs = JobPosition.query.filter_by(
        status="approved"
    ).all()

    result = []

    for job in jobs:

        company = Company.query.get(
            job.company_id
        )

        existing_application = Application.query.filter_by(
            student_id=student.id,
            job_id=job.id
        ).first()

        if existing_application:

            applied = True

            application_status = existing_application.status

        else:

            applied = False

            application_status = ""

        result.append({

            "id": job.id,

            "title": job.title,

            "company": company.company_name,

            "location": job.location,

            "salary": job.salary,

            "description": job.description,

            "applied": applied,

            "application_status": application_status

        })

    return jsonify(result)

@stu_bp.route("/student/search-jobs")
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def student_search_jobs():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    query = request.args.get("query")

    jobs = JobPosition.query.filter(
        (
            JobPosition.title.ilike(f"%{query}%")
        ) |
        (
            JobPosition.required_skills.ilike(f"%{query}%")
        )
    ).filter_by(
        status="approved"
    ).all()

    result = []

    for job in jobs:

        company = Company.query.get(
            job.company_id
        )

        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": company.company_name,
            "required_skills": job.required_skills,
            "location": job.location,
            "salary": job.salary
        })

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
            "interview_date": application.interview_date,
            "feedback": application.feedback
        })

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

    return jsonify({

        "message": "CSV export started",

        "task_id": task.id
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
            "message": "No file uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "Empty filename"
        }), 400

    filename = secure_filename(file.filename)

    upload_path = os.path.join(
        "uploads",
        filename
    )

    file.save(upload_path)

    student.resume = filename

    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": filename
    })
