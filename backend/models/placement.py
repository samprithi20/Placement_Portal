from database import db

class Placement(db.Model):
    __tablename__ = "placement"
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    position = db.Column(db.String(100))

    salary = db.Column(db.String(100))

    joining_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, server_default = db.func.now())