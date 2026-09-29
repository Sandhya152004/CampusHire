from celery.schedules import crontab
from celery_config import celery

celery.conf.beat_schedule = {

    "daily-interview-reminders": {

        "task": "tasks.send_interview_reminders",

        "schedule": crontab(hour=9, minute=0)

    },

    "monthly-placement-report": {

        "task": "tasks.send_monthly_report",

        "schedule": crontab(
            day_of_month=1,
            hour=9,
            minute=0
        )

    }

}