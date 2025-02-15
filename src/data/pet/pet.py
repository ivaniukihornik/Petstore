from dataclasses import dataclass

from src.data.pet.category import Category
from src.data.pet.tag import Tag


@dataclass
class Pet:
    id: int
    category: Category
    name: str
    photo_urls: list[str]
    tags: list[Tag]
    status: str

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        return {
            'id': self.id,
            'category': self.category if isinstance(self.category, dict) else self.category.to_dict(),
            'name': self.name,
            'photoUrls': self.photo_urls,
            'tags': [tag if isinstance(tag, dict) else tag.to_dict() for tag in self.tags],
            'status': self.status
        }
