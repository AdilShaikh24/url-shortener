"""
utils.py
Contain utility methods for the project.
"""

# Standard Library Imports
import logging

from rest_framework.exceptions import ValidationError
# Third Party Imports
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def get_request_data(request):
    """Returns formatted JSON request data"""
    try:
        data = request.data
    except Exception as e:
        logger.error(f"An exception occurred while parsing JSON: {e}")
        raise ValidationError("An invalid JSON payload has been provided.")
    return data


def format_response(data, message, status_code, success=True):
    """
    Formats incoming parameters into a consistent response
    :param data:
    :param message:
    :param status_code: Status code of application request
    :return: Returns a uniform response for all handled cases.
    """

    logger.debug("Formatted response")
    logger.debug(f"HTTP Status Code: {status_code}")
    logger.debug(f"Message: {message}")
    logger.debug(f"Data: {data}")
    logger.debug(f"Success: {success}")

    response = Response(
        data={
            "status_code": status_code,
            "message": message,
            "data": data,
            "success": success,
        },
        status=status_code,
    )
    return response
