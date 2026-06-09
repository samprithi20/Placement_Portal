from celery_worker import celery

from app import app

from models.application import Application
from models.student import Student
from models.company import Company
from models.job_position import JobPosition

import pandas as pd
import os
#import os
from datetime import datetime, timedelta


@celery.task
def send_interview_reminders():

    with app.app_context():

        applications = Application.query.filter_by(
            status="interview scheduled"
        ).all()

        for application in applications:

            student = Student.query.get(
                application.student_id
            )

            job = JobPosition.query.get(
                application.job_id
            )

            company = Company.query.get(
                job.company_id
            )

            reminder_message = f"""
            Interview Reminder

            Student: {student.full_name}

            Company: {company.company_name}

            Job Role: {job.title}

            Interview Date:
            {application.interview_date}
            """

            print(reminder_message)

    return "Interview reminders sent"

@celery.task
def generate_monthly_report():

    with app.app_context():

        companies = Company.query.all()

        report_html = """
        <html>
        <head>
            <title>Monthly Placement Report</title>
        </head>

        <body>

            <h1>Monthly Placement Report</h1>

            <hr>
        """

        for company in companies:

            jobs = JobPosition.query.filter_by(
                company_id=company.id
            ).all()

            job_ids = [job.id for job in jobs]

            total_applications = 0
            total_placed = 0

            if job_ids:

                total_applications = Application.query.filter(
                    Application.job_id.in_(job_ids)
                ).count()

                total_placed = Application.query.filter(
                    Application.job_id.in_(job_ids),
                    Application.status == "placed"
                ).count()

            report_html += f"""
                <h2>Company: {company.company_name}</h2>

                <p>Total Jobs: {len(jobs)}</p>

                <p>Total Applications: {total_applications}</p>

                <p>Total Placed Students: {total_placed}</p>

                <hr>
            """

        report_html += """
        </body>
        </html>
        """

        os.makedirs(
            "reports",
            exist_ok=True
        )

        filename = "reports/monthly_report.html"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report_html)

        print(
            f"Placement report generated: {filename}"
        )

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

        filename = f"student_{student_id}.csv"

        filepath = os.path.join(
            "exports",
            filename
        )

        df.to_csv(
            filepath,
            index=False
        )

        print(
            f"CSV export completed: {filepath}"
        )

    return filepath