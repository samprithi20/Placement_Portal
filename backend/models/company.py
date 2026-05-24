from database import db

class Company(db.Model):

    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    company_name = db.Column(db.String(100), nullable=False)

    industry = db.Column(db.String(100))

    location = db.Column(db.String(100))

    website = db.Column(db.String(200))

    hr_name = db.Column(db.String(100))

    hr_email = db.Column(db.String(100))

    approval_status = db.Column(db.String(20), default="pending")