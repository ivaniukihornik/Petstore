from requests import Response

from src.data.pet.pet import Pet
from src.json_schemas.pet_schemas import pet_schema
from utils.base_api import BaseApi


class PetApi(BaseApi):
    def __init__(self):
        super().__init__()
        self.__endpoint = '/pet'

    def get_pet(self, pet_id: int) -> Response:
        """
        Retrieves a pet by its ID.
        :param pet_id: Pet ID
        :return: API response
        """
        return self._send_request(method='GET', endpoint=f'{self.__endpoint}/{pet_id}')

    def add_pet(self, pet: Pet, is_unsupported_content_type: bool = False) -> Response:
        """
        Adds a new pet.
        :param pet: Pet object to add
        :param is_unsupported_content_type: Flag for unsupported content type
        :return: API response
        """
        request_body = pet.to_dict()
        headers = {'Content-Type': 'text/html'} if is_unsupported_content_type else {}
        return self._send_request(method='POST', endpoint=self.__endpoint, headers=headers, json=request_body)

    def validate_pet_schema(self, response_body: dict) -> bool:
        """
        Validates the response schema for a pet.
        :param response_body: Response body to validate
        :return: True if valid, False otherwise
        """
        return self._validate_schema_of_response_body(response_body, pet_schema)

    def update_pet(self, pet: Pet | dict, is_unsupported_content_type: bool = False) -> Response:
        """
        Updates an existing pet.
        :param pet: Pet object or dictionary to update
        :param is_unsupported_content_type: Flag for unsupported content type
        :return: API response
        """
        request_body = pet.to_dict()
        headers = {'Content-Type': 'text/html'} if is_unsupported_content_type else {}
        return self._send_request(method='PUT', endpoint=self.__endpoint, headers=headers, json=request_body)

    def delete_pet(self, pet_id: int) -> Response:
        """
        Deletes a pet by its ID.
        :param pet_id: Pet ID to delete
        :return: API response
        """
        return self._send_request(method='DELETE', endpoint=f'{self.__endpoint}/{pet_id}')

    def is_pet_exist(self, pet_id: int) -> bool:
        """
        Checks if a pet exists by its ID.
        :param pet_id: Pet ID to check
        :return: True if pet exists, False otherwise
        """
        response = self.get_pet(pet_id)
        return response.status_code == 200 and response.json().get('id') == pet_id
