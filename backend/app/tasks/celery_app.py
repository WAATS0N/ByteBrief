from celery import Celery
from app.core.config import settings

# MongoDB as both broker and result backend — no Redis required
app = Celery(
    "bytebrief",
    broker=f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/bytebrief_celery",
    backend=f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/bytebrief_celery",
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "scrape-all-sources": {
            "task": "app.tasks.scrape_tasks.scrape_all_sources",
            "schedule": settings.SCRAPE_INTERVAL_MINUTES * 60.0,
        },
    },
)

# Discover tasks
app.autodiscover_tasks(["app.tasks.scrape_tasks", "app.tasks.nlp_tasks"])
