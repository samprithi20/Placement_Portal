from celery import Celery

celery = Celery(
    "placement_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {

    "daily-interview-reminder": {

        "task": "tasks.send_interview_reminders",

        "schedule": 60.0
    },

    "monthly-placement-report": {

        "task": "tasks.generate_monthly_report",

        "schedule": 120.0
    }
}