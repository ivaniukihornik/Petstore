import logging
from typing import Callable

import jsonschema as jsonschema
import requests
from deepdiff import DeepDiff


class BaseApi:
    def __init__(self):
        self.__api_name = 'Petstore'
        self.__base_url = 'https://petstore.swagger.io/v2'

    @staticmethod
    def log_api_call(request_method: Callable):
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
            url = self.__base_url + kwargs.get('endpoint')
            headers = kwargs.get('headers', {})
            json = kwargs.get('json', {})
            request_method_name = request_method.__name__
            if 'get' in request_method_name:
                method = 'GET'
            elif 'post' in request_method_name:
                method = 'POST'
            elif 'put' in request_method_name:
                method = 'PUT'
            elif 'delete' in request_method_name:
                method = 'DELETE'
            else:
                raise ValueError('Unexpected method. Check name of the request method.')
            logging.info(
                f'{self.__api_name} API\nREQUEST: {method} {url}\nHeaders: {headers}\nJson body: {json}')
            response = request_method(self, **kwargs)
            logging.info(f'{self.__api_name} API\nRESPONSE: {response.status_code} {response.reason}\nHeaders: '
                         f'{response.headers}\nResponse body: {response.text}')
            return response

        return _log_wrapper

    @log_api_call
    def _get(self, endpoint: str) -> requests.Response:
        """
        Sends a GET request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :return: The response object from the request.
        """
        return requests.get(url=self.__base_url + endpoint)

    @log_api_call
    def _post(self, endpoint: str, headers: dict = None, json: dict = None) -> requests.Response:
        """
        Sends a POST request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :param headers: The request headers (optional).
        :param json: The JSON payload to include in the request (optional).
        :return: The response object from the request.
        """
        return requests.post(url=self.__base_url + endpoint, headers=headers, json=json)

    @log_api_call
    def _put(self, endpoint: str, headers: dict = None, json: dict = None) -> requests.Response:
        """
        Sends a PUT request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :param headers: The request headers (optional).
        :param json: The JSON payload to include in the request (optional).
        :return: The response object from the request.
        """
        return requests.put(url=self.__base_url + endpoint, headers=headers, json=json)

    @log_api_call
    def _delete(self, endpoint: str) -> requests.Response:
        """
        Sends a DELETE request to the specified API endpoint.
        :param endpoint: The API endpoint to send the request to.
        :return: The response object from the request.
        """
        return requests.delete(url=self.__base_url + endpoint)

    @staticmethod
    def _validate_schema_of_response_body(response_body: dict, schema: dict) -> bool | None:
        """
        Validates the response body against a given schema.
        :param response_body: Response body to validate.
        :param schema: JSON schema to validate against.
        :return: True if valid, raises AssertionError if invalid.
        """
        try:
            jsonschema.validate(response_body, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise AssertionError(f'Wrong JSON schema: \n {e}')
        else:
            return True

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
