'''from database import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.Text)
    resume_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    applications = db.relationship(
    "Application",
    backref="student",
    lazy=True
    )
    placements = db.relationship(
    "Placement",
    backref="student",
    lazy=True
    )
    '''

from database import db


class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    department = db.Column(
        db.String(100)
    )

    cgpa = db.Column(
        db.Float
    )

    graduation_year = db.Column(
        db.Integer
    )

    skills = db.Column(
        db.Text
    )