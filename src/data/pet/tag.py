from dataclasses import dataclass

from utils.random_data_generator import generate_random_id


@dataclass
class Tag:
    id: int = generate_random_id()
    name: str = f'Tag_{id}'

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        return self.__dict__
