import pytest
from utils.logger import logger
from src.resources.pet_api import PetApi


@pytest.fixture
def create_pet_api() -> PetApi:
    """
    Creates and returns an instance of the PetApi.
    :return: PetApi instance
    """
    return PetApi()


def pytest_runtest_setup(item):
    """Logs the start of a test."""
    logger.info(f'Test started: {item.name}')


def pytest_runtest_teardown(item):
    """Logs the end of a test."""
    logger.info(f'Test finished: {item.name}')
