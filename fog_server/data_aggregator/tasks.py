# Inside code/fog_server/data_aggregator/tasks.py
import requests
from celery import shared_task
import logging # Import logging

logger = logging.getLogger(__name__) # Get a logger

CLOUD_API_URL = "http://127.0.0.1:8001/care/receive_fog_data/"

@shared_task
def process_edge_data(data):
    try:
        print("Processing edge data...")
        print("Data:", data)
        response = requests.post(CLOUD_API_URL, json=data, timeout=1) # Added timeout
        print("Data sent to cloud:", response.status_code)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data to cloud: {e}") # Modified Log
        try:
            self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded for sending data to cloud.")
    except Exception as e: # ADDED broader exception catch
            logger.error(f"An unexpected error occurred in process_edge_data: {e}", exc_info=True)