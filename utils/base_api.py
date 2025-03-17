import jsonschema as jsonschema
import requests
from deepdiff import DeepDiff

from utils.logger import log_api_call_wrapper


class BaseApi:
    def __init__(self):
        self._api_name = 'Petstore'
        self._base_url = 'https://petstore.swagger.io/v2'

    @log_api_call_wrapper
    def _get(self, endpoint: str) -> requests.Response:
        """
        Sends a GET request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :return: The response object from the request.
        """
        return requests.get(url=self._base_url + endpoint)

    @log_api_call_wrapper
    def _post(self, endpoint: str, headers: dict = None, json: dict = None) -> requests.Response:
        """
        Sends a POST request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :param headers: The request headers (optional).
        :param json: The JSON payload to include in the request (optional).
        :return: The response object from the request.
        """
        return requests.post(url=self._base_url + endpoint, headers=headers, json=json)

    @log_api_call_wrapper
    def _put(self, endpoint: str, headers: dict = None, json: dict = None) -> requests.Response:
        """
        Sends a PUT request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :param headers: The request headers (optional).
        :param json: The JSON payload to include in the request (optional).
        :return: The response object from the request.
        """
        return requests.put(url=self._base_url + endpoint, headers=headers, json=json)

    @log_api_call_wrapper
    def _delete(self, endpoint: str) -> requests.Response:
        """
        Sends a DELETE request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :return: The response object from the request.
        """
        return requests.delete(url=self._base_url + endpoint)

    @staticmethod
    def _validate_schema_of_response_body(response_body: dict, schema: dict) -> None:
        """
        Validates the response body against a given schema.
        :param response_body: Response body to validate.
        :param schema: JSON schema to validate against.
        :return: None
        """
        return jsonschema.validate(response_body, schema)

    @staticmethod
    def validate_dict_data(expected_data: dict, actual_data: dict) -> bool | None:
        """
        Validates that two dictionaries match.
        :param expected_data: The expected dictionary data.
        :param actual_data: The actual dictionary data received.
        :return: True if dictionaries match, raises AssertionError and show differences if they exist.
        """
        if actual_data == expected_data:
            return True
        else:
            diffs = DeepDiff(actual_data, expected_data, ignore_order=True)
            raise AssertionError(f'Actual data doesn\'t match the expected. Differences are: {diffs}')
