from database import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # 👨‍🎓 Student applying
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    # 💼 Job they applied to
    job_id = db.Column(db.Integer, db.ForeignKey("job_positions.id"), nullable=False)

    # 📊 Application status
    status = db.Column(db.String(20), default="applied")
    # applied / shortlisted / selected / rejected

    applied_at = db.Column(db.DateTime, server_default=db.func.now())