import os
from celery import Celery
from beat_schedule import beat_schedule


def make_celery():
    redis_url = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    celery = Celery(
        "placement_portal",
        broker=redis_url,
        backend=redis_url
    )

    celery.conf.beat_schedule = beat_schedule

    celery.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=False
    )

    return celery


celery = make_celery()