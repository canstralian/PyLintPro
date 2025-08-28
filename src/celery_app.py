# src/celery_app.py

"""
Celery application for background task processing in Mendicant AI.
Handles repository analysis and automated remediation tasks.
"""

import os
from celery import Celery
from pathlib import Path

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent))

from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from utils import setup_logging

logger = setup_logging(__name__)

# Create Celery app
app = Celery(
    'mendicant',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        'src.tasks.repository_analysis',
        'src.tasks.automated_fixes',
        'src.tasks.health_monitoring'
    ]
)

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    task_compression='gzip',
    result_compression='gzip',
    result_expires=3600,  # 1 hour
)

# Configure beat schedule for periodic tasks
app.conf.beat_schedule = {
    'health-check-active-repos': {
        'task': 'src.tasks.health_monitoring.check_active_repositories',
        'schedule': 3600.0,  # Run every hour
    },
    'update-scoreboard': {
        'task': 'src.tasks.health_monitoring.update_public_scoreboard',
        'schedule': 86400.0,  # Run daily
    },
}

if __name__ == '__main__':
    app.start()