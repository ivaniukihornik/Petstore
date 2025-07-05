from dataclasses import dataclass

from utils.random_data_generator import generate_random_id, get_random_animal_category


@dataclass
class Category:
    id: int = generate_random_id()
    name: str = get_random_animal_category()

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        return self.__dict__
