from dataclasses import dataclass

from src.data.pet.category import Category
from src.data.pet.tag import Tag


@dataclass
class Pet:
    id: int
    category: Category | dict
    name: str
    photoUrls: list[str]
    tags: list[Tag] | list[dict]
    status: str

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        self.category = self.category if isinstance(self.category, dict) else self.category.to_dict()
        self.tags = [tag if isinstance(tag, dict) else tag.to_dict() for tag in self.tags]

        return self.__dict__
