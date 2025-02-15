import logging
from typing import Literal

import jsonschema as jsonschema
import requests
from requests import Response


class BaseApi:
    def __init__(self):
        self.__api_name = 'Petstore'
        self.__base_url = 'https://petstore.swagger.io/v2'

    def _log_request(self, method: str, url: str, headers: dict, json: dict) -> None:
        """
        Logs the details of an API request.
        :param method: HTTP method
        :param url: Request URL
        :param headers: Request headers
        :param json: JSON body of the request
        """
        logging.info(f'{self.__api_name} API. REQUEST:\nMethod: {method}\nUrl: {url}\nHeaders: {headers}\nJson body: '
                     f'{json}')

    def _log_response(self, response: Response) -> None:
        """
        Logs the details of an API response.
        :param response: Response object from the API call
        """
        logging.info(f'{self.__api_name} API. RESPONSE:\nStatus code: {response.status_code}\nHeaders: '
                     f'{response.headers}\nResponse body: {response.text}')

    def _send_request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], endpoint: str, headers: dict = None,
                      json: dict = None) -> Response:
        """
        Sends an HTTP request to the specified endpoint.
        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param endpoint: API endpoint
        :param headers: Optional request headers
        :param json: Optional JSON body for the request
        :return: API response
        """
        url = self.__base_url + endpoint
        self._log_request(method=method, url=url, headers=headers, json=json)
        response = requests.request(method=method, url=url, headers=headers, json=json)
        self._log_response(response)
        return response

    @staticmethod
    def _validate_schema_of_response_body(response_body: dict, schema: dict) -> bool:
        """
        Validates the response body against a given schema.
        :param response_body: Response body to validate
        :param schema: JSON schema to validate against
        :return: True if valid, raises AssertionError if invalid
        """
        try:
            jsonschema.validate(response_body, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise AssertionError(f'Wrong JSON schema: \n {e}')
        else:
            return True
