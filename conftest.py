from typing import Callable, Literal

import pytest
from utils.logger import logger
from src.resources.pet_api import PetApi

from src.data.pet.category import Category
from src.data.pet.pet import Pet
from src.data.pet.tag import Tag
from utils.random_data_generator import generate_random_id


@pytest.fixture
def create_pet_api() -> PetApi:
    """
    Creates and returns an instance of the PetApi.
    :return: PetApi instance
    """
    return PetApi()


@pytest.fixture()
def pc_generate_pet_object() -> Callable:
    """
    Generates a Pet object with various data.
    :return: Callable function that generates a Pet object based on provided parameters.
    """

    def _generate_pet_object(data: Literal['new', 'update'], pet_id: int = None, fields_to_replace: dict = None) -> Pet:
        """
        Generates a Pet object with new data or data for updating.
        :param data: Type of pet data ('new' or 'update').
        :param pet_id: Optional pet ID. If None, a random ID is generated.
        :param fields_to_replace: Optional dictionary to override specific pet fields.
        :return: Generated Pet object.
        """
        if not pet_id and pet_id != 0:
            pet_id = generate_random_id()
        match data:
            case 'new':
                pet = Pet(id=pet_id)
            case 'update':
                pet = Pet(id=pet_id,
                          category=Category(1000, 'UPDATED_CATEGORY'),
                          name='UPDATED_NAME',
                          photoUrls=['https://UPDATEDphoto1.jpg', 'https://UPDATEDphoto2.jpg'],
                          tags=[Tag(1, 'UPDATED_TAG1'), Tag(2, 'UPDATED_TAG2')],
                          status='UPDATED')
            case _:
                raise ValueError('Unknown "data" argument. Pass a valid value.')
        if fields_to_replace:
            for key, value in fields_to_replace.items():
                setattr(pet, key, value)

        return pet

    return _generate_pet_object


@pytest.fixture()
def pc_create_new_pet(create_pet_api, pc_generate_pet_object) -> Pet:
    """
    Creates a new pet in API. If the pet already exists, it is deleted and re-added.
    :param create_pet_api: Instance of PetApi fixture.
    :param pc_generate_pet_object: Function to generate a Pet object.
    :return: Created pet object.
    """
    api = create_pet_api
    pet = pc_generate_pet_object(data='new')
    if not api.is_pet_exist(pet.id):
        api.add_pet(pet)
    else:
        api.delete_pet(pet.id)
        api.add_pet(pet)
    return pet


@pytest.fixture()
def pc_delete_pet_if_exists(create_pet_api) -> Callable:
    """
    Deletes a pet if it exists in API.
    :param create_pet_api: Instance of PetApi fixture.
    :return: Callable function that deletes a pet by ID if it exists.
    """

    def _delete_pet(pet_id: int = None) -> int:
        """
        Deletes a pet if it exists.
        :param pet_id: ID of the pet to delete. If None, a random ID is generated.
        :return: The pet ID that was checked for deletion.
        """
        api = create_pet_api
        if not pet_id and pet_id != 0:
            pet_id = generate_random_id()
        if api.is_pet_exist(pet_id):
            api.delete_pet(pet_id)
        return pet_id

    return _delete_pet


def pytest_runtest_setup(item):
    """Logs the start of a test."""
    logger.info(f'Test started: {item.name}')


def pytest_runtest_teardown(item):
    """Logs the end of a test."""
    logger.info(f'Test finished: {item.name}\n')
