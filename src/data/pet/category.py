from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        return self.__dict__
