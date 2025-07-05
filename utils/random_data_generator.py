import random

from constants import MIN_API_ID, MAX_API_ID


def generate_random_id() -> int:
    """
    Generates random available ID
    :return: ID integer
    """
    return random.randint(MIN_API_ID, MAX_API_ID)


def get_random_animal_category() -> str:
    """
    Returns random category from list of available
    :return: Random category
    """
    return random.choice(["Dog", "Cat", "Elephant", "Tiger", "Dolphin", "Giraffe", "Panda", "Chicken", "Lion", "Zebra"])
