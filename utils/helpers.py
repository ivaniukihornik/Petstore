import random


def get_random_number(min_value: int, max_value: int) -> int:
    """
    Returns random integer from a specified range
    :param min_value: minimal range limit
    :param max_value: maximal range limit
    :return:
    """
    return random.randint(min_value, max_value)
