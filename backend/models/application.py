from database import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey("job_position.id"), nullable=False)

    status = db.Column(db.String(50), default="Applied")

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    feedback = db.Column(db.Text)

    interview_date = db.Column(db.String(100))