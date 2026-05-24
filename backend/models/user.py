from database import db

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True,nullable=False)

    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20),nullable=False)

    is_active = db.Column(db.Boolean,default=True)

    is_blacklisted = db.Column(db.Boolean,default=False)