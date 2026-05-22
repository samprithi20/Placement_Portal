from database import db

class Placement(db.Model):
    __tablename__ = "placements"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    position = db.Column(db.String(100))
    salary = db.Column(db.Float)
    joining_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())