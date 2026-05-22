from database import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job_positions.id"), nullable=False)
    status = db.Column(db.String(20), default="applied")
    applied_at = db.Column(db.DateTime, server_default=db.func.now())