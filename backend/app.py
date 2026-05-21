from flask import Flask
from config import Config
from database import db
from models import User, Student, Company, JobPosition, Application, Placement

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return "Placement Portal Running"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)