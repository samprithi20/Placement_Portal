from database import db

class JobPosition(db.Model):

    __tablename__ = "job_position"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    location = db.Column(db.String(100))

    salary = db.Column(db.String(100))

    status = db.Column(db.String(50), default="pending")

    required_skills = db.Column(db.Text)

    experience_required = db.Column(db.String(100))

    benefits = db.Column(db.Text)

    eligible_department = db.Column(db.String(100))

    minimum_cgpa = db.Column(db.Float)

    eligible_batch = db.Column(db.Integer)