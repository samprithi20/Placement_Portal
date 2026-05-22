from app import app
from database import db
from models.user import User

with app.app_context():
    admin = User.query.filter_by(role="admin").first()

    if admin:
        print("Admin already exists")
    else:
        new_admin = User(
            email="admin@placement.com",
            password="admin123",   
            role="admin"
        )

        db.session.add(new_admin)
        db.session.commit()

        print("Admin created successfully")