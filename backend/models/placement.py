from database import db

class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    # 👨‍🎓 Student who got placed
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    # 🏢 Company offering job
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    # 💼 Role offered
    position = db.Column(db.String(100))

    # 💰 Salary offered
    salary = db.Column(db.Float)

    # 📅 Joining date
    joining_date = db.Column(db.Date)

    created_at = db.Column(db.DateTime, server_default=db.func.now())