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

#with app.app_context():
 #   db.create_all() 

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

    total_applications = Application.query.count()

    return jsonify({
    "total_students": total_students,
    "total_companies": total_companies,
    "total_jobs": total_jobs,
    "total_applications": total_applications,
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

@app.route("/company/create-job", methods=["POST"])
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

    status="pending"
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job created and waiting for admin approval"
    })

@app.route("/admin/pending-jobs")
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

@app.route("/admin/approve-job/<int:job_id>", methods=["PUT"])
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

    return jsonify({
        "message": "Job approved successfully"
    })

@app.route("/admin/reject-job/<int:job_id>", methods=["DELETE"])
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

    return jsonify({
        "message": "Job removed successfully"
    })

@app.route("/admin/jobs")
@jwt_required()
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

@app.route("/admin/search-jobs")
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

@app.route("/admin/applications")
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

@app.route("/admin/reject-company/<int:company_id>", methods=["DELETE"])
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

    return jsonify({
        "message": "Company removed successfully"
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

@app.route("/admin/companies")
@jwt_required()
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

@app.route("/admin/search-companies")
@jwt_required()
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

@app.route("/admin/students")
@jwt_required()
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

@app.route("/admin/search-students")
@jwt_required()
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

@app.route("/admin/deactivate-user/<int:user_id>", methods=["PUT"])
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

    return jsonify({
        "message": "User deactivated"
    })

@app.route("/admin/blacklist-user/<int:user_id>", methods=["PUT"])
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

    return jsonify({
        "message": "User blacklisted successfully"
    })

@app.route("/student/apply-job/<int:job_id>", methods=["POST"])
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
            "message": "Job not available"
        }), 400

    existing_application = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if existing_application:
        return jsonify({
            "message": "Already applied"
        }), 400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="applied"
    )

    db.session.add(application)

    db.session.commit()

    return jsonify({
        "message": "Applied successfully"
    })

@app.route("/company/jobs")
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
            "applications": application_count
        })

    return jsonify(result)

@app.route("/company/job-applications/<int:job_id>")
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
            "interview_date": application.interview_date
        })

    return jsonify(result)

@app.route("/company/update-application/<int:application_id>", methods=["PUT"])
@jwt_required()
def update_application(application_id):

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

    application.status = data["status"]

    application.feedback = data.get("feedback")

    db.session.commit()

    return jsonify({
        "message": "Application updated successfully"
    })

@app.route("/company/schedule-interview/<int:application_id>", methods=["PUT"])
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

    db.session.commit()

    return jsonify({
        "message": "Interview scheduled"
    })

@app.route("/company/close-job/<int:job_id>", methods=["PUT"])
@jwt_required()
def close_job(job_id):

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "company":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    job.status = "closed"

    db.session.commit()

    return jsonify({
        "message": "Job closed successfully"
    })

@app.route("/student/jobs")
@jwt_required()
def approved_jobs():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user.role != "student":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    jobs = JobPosition.query.filter_by(
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
            "company": company.company_name,
            "location": job.location,
            "salary": job.salary
        })

    return jsonify(result)

@app.route("/student/my-applications")
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
            "interview_date": application.interview_date
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)