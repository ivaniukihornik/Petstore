from dataclasses import dataclass, field

from src.data.pet.category import Category
from src.data.pet.tag import Tag
import names


@dataclass
class Pet:
    id: int
    category: Category | dict = field(default_factory=Category)
    name: str = names.get_first_name()
    photoUrls: list[str] = field(default_factory=lambda: ['https://photo1.jpg', 'https://photo2.jpg'])
    tags: list[Tag] | list[dict] = field(default_factory=lambda: [Tag(), Tag()])
    status: str = 'available'

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        self.category = self.category if isinstance(self.category, dict) else self.category.to_dict()
        self.tags = [tag if isinstance(tag, dict) else tag.to_dict() for tag in self.tags]

        return self.__dict__
