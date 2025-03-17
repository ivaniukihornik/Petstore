import logging

from constants import ROOT_DIR, REQUEST_METHODS_MAPPING
from typing import Callable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f'{ROOT_DIR}/test.log'),
    ]
)

logger = logging.getLogger(__name__)


def log_api_call_wrapper(request_method: Callable):
    """
    Decorator that logs API request and response details.
    :param request_method: The HTTP request method to be wrapped.
    :return: A wrapped function that logs request and response details.
    """

    def _log_wrapper(self, **kwargs):
        """
        Logs API request details and captures the response.
        :param kwargs: Dictionary of request parameters.
        :return: Response object from the request.
        """
        url = self._base_url + kwargs.get('endpoint')
        headers = kwargs.get('headers', {})
        json = kwargs.get('json', {})
        method = REQUEST_METHODS_MAPPING.get(request_method.__name__)
        if not method:
            raise ValueError('Unexpected method. Check name of the request method.')
        logging.info(
            f'{self._api_name} API\nREQUEST: {method} {url}\nHeaders: {headers}\nJson body: {json}')
        response = request_method(self, **kwargs)
        logging.info(f'{self._api_name} API\nRESPONSE: {response.status_code} {response.reason}\nHeaders: '
                     f'{response.headers}\nResponse body: {response.text}')
        return response

    return _log_wrapper
