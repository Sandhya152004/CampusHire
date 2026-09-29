from app import app
from celery_config import celery

app.app_context().push()

import tasks

import celery_beat