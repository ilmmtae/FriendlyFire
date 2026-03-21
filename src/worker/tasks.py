import time
import logging
import httpx
from src.core.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="send_invite_email_task")
def send_invite_email_task(email: str, invite_code: str, first_name: str, last_name: str):
    logger.info(f"--- [WORKER] Starting email task for {email} ---")
    start_time = time.perf_counter()

    invite_sync_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "invite_code": invite_code
    }

    with httpx.Client() as client:
        try:
            response = client.post(
                "http://127.0.0.1:8000/api/internal/invite/",
                json=invite_sync_data,
                timeout=10.0
            )
            response.raise_for_status()
            logger.info(f"--- [WORKER] Successfully synced to Django for {email} ---")
        except Exception as e:
            logger.error(f"--- [WORKER] Django Sync Error: {e} ---")
            raise

    end_time = time.perf_counter()
    logger.info(f"--- [WORKER] Task finished in {end_time - start_time:.4f}s ---")