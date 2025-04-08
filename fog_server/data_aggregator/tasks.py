# Modified fog_server/data_aggregator/tasks.py
import requests
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
import logging

logger = logging.getLogger(__name__)

CLOUD_API_URL = "http://127.0.0.1:8001/care/receive_fog_data/"

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_edge_data(self, data):
    try:
        print("task area {}")
        # Make sure the data format matches what the cloud server expects
        response = requests.post(CLOUD_API_URL, json=data, timeout=5)
        logger.info(f"Data sent to cloud: {response.status_code}")
        
        # Log the response content for debugging
        logger.info(f"Cloud server response: {response.text}")

        
        print(response.raise_for_status())
        return f"Data successfully sent to cloud: {response.status_code}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data to cloud: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=self.request.retries * 5)
    except Exception as e:
        logger.error(f"Unexpected error in process_edge_data: {e}", exc_info=True)
        raise