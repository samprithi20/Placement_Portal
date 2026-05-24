from database import db
'''
class JobPosition(db.Model):
    __tablename__ = "job_positions"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.Float)
    skills_required = db.Column(db.Text)
    eligibility_cgpa = db.Column(db.Float)
    eligible_department = db.Column(db.String(100))
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    applications = db.relationship(
    "Application",
    backref="job_position",
    lazy=True
    )
    status = db.Column(db.String(50), default="pending")
'''
#from database import db


#from database import db


class JobPosition(db.Model):

    __tablename__ = "job_position"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(100)
    )

    salary = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50),
        default="pending"
    )

    required_skills = db.Column(db.Text)

    experience_required = db.Column(db.String(100))

    benefits = db.Column(db.Text)