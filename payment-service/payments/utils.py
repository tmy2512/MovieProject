import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_booking_info(booking_id):
    try:
        response = requests.get(
            f"{settings.BOOKING_SERVICE_URL}/api/bookings/{booking_id}/",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to get booking info: {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting booking info: {str(e)}")
        return None 