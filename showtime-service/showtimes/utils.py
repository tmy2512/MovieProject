import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_movie_info(movie_id):
    try:
        response = requests.get(
            f"{settings.MOVIE_SERVICE_URL}/api/movies/{movie_id}/",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to get movie info: {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting movie info: {str(e)}")
        return None
