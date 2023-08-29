import os


REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

REDIS_CELERY_BROKER_URL = f"{REDIS_URL}/0"
REDIS_CELERY_BACKEND_URL = f"{REDIS_URL}/1"
REDIS_DATA_URL = f"{REDIS_URL}/2"

REDIS_EXPIRY = 3600

SHOW_DDK_EDITOR = os.environ.get("SHOW_DDK_EDITOR", True)