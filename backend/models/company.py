from database import db

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    hr_name = db.Column(db.String(100))
    hr_email = db.Column(db.String(120))
    approval_status = db.Column(db.String(20), default="pending")
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    placements = db.relationship(
    "Placement",
    backref="company",
    lazy=True
    )