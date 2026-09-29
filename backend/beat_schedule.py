from celery.schedules import crontab

beat_schedule = {

    "daily-interview-reminder": {

        "task": "tasks.send_interview_reminders",

        "schedule": crontab(

            hour=9,

            minute=0

        )

    }

}