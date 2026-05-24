from database import db

class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    full_name = db.Column(db.String(100),nullable=False)

    department = db.Column(db.String(100))

    cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    skills = db.Column(db.Text)