from celery_worker import celery

from app import app

from models.application import Application
from models.student import Student
from models.company import Company
from models.job_position import JobPosition

import pandas as pd
import os
#import os
from datetime import datetime


@celery.task
def send_interview_reminders():

    interviews = [
        {
            "student": "Sam",
            "company": "TCS",
            "job": "Python Developer",
            "date": "2026-06-01",
            "time": "10:00 AM",
            "email": "sam@example.com"
        }
    ]

    for interview in interviews:

        reminder_message = f"""
                Interview Reminder

                Hello {interview['student']},

                This is a reminder for your upcoming interview.

                Company: {interview['company']}
                Role: {interview['job']}
                Date: {interview['date']}
                Time: {interview['time']}

                Best of luck!

                Placement Portal
                """

        print(reminder_message)

    return "Interview reminders sent"


@celery.task
def generate_monthly_report():

    report_html = """
    <html>
    <head>
        <title>Placement Report</title>
    </head>

    <body>

        <h1>Monthly Placement Report</h1>

        <hr>

        <h2>Company: TCS</h2>

        <p>Total Applications: 120</p>

        <p>Students Shortlisted: 45</p>

        <p>Students Placed: 20</p>

        <p>Average Package: 8 LPA</p>

    </body>
    </html>
    """

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_html)

    print(f"Placement report generated: {filename}")

    return filename


@celery.task(name="tasks.export_student_csv")
def export_student_csv(student_id):

    with app.app_context():

        applications = Application.query.filter_by(
            student_id=student_id
        ).all()

        data = []

        for application in applications:

            job = JobPosition.query.get(
                application.job_id
            )

            company = Company.query.get(
                job.company_id
            )

            data.append({

                "Company": company.company_name,

                "Job": job.title,

                "Status": application.status,

                "Interview Date": application.interview_date
            })

        df = pd.DataFrame(data)

        os.makedirs("exports", exist_ok=True)

        filename = f"exports/student_{student_id}.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(
            f"CSV export completed: {filename}"
        )

    return filename