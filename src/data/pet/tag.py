from dataclasses import dataclass


@dataclass
class Tag:
    id: int
    name: str

    def to_dict(self) -> dict:
        """
        Represents data object in dictionary
        :return: dict respresentation
        """
        return {
            'id': self.id,
            'name': self.name
        }
