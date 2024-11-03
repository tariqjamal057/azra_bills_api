


import uuid
from enum import Enum

def uuid_generator():
    return str(uuid.uuid4())


class BaseEnum(Enum):

    @property
    def name(self):
        return self._name_.replace("_", " ").title()
    
    @classmethod
    def get_name_by_value(cls: type[Enum], value):
        for member in cls:
            if member.value == value:
                return member.name
        return None
    
    @classmethod
    def all(cls: type[Enum]):
        return [{"id": member.value, "name": member.name} for member in cls]
    
    @classmethod
    def all_ids(cls):
        return [member.value for member in cls]
    
    @classmethod
    def all_names(cls):
        return [member.name for member in cls]