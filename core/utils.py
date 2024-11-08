import os
import time
import uuid
from enum import Enum

from sqlalchemy import CHAR, TypeDecorator


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


class ULIDGenerator:
    """Class to generate ULIDs based on timestamp and randomness."""

    BASE32_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    @classmethod
    def encode_base32(cls, number, length):
        """Encodes a number into Crockford's Base32, padding to a fixed length."""
        encoded = ""
        while number > 0:
            number, remainder = divmod(number, 32)
            encoded = cls.BASE32_ALPHABET[remainder] + encoded
        return encoded.zfill(length)

    @classmethod
    def generate(cls):
        """Generates a ULID as a 26-character string."""
        # Get the current timestamp in milliseconds (48 bits)
        timestamp = int(time.time() * 1000)

        # Generate 10 random bytes for the unique part (80 bits)
        random_bytes = os.urandom(10)
        random_number = int.from_bytes(random_bytes, "big")

        # Convert timestamp and random number to Base32 (Crockford) encoding
        timestamp_encoded = cls.encode_base32(timestamp, 10)
        randomness_encoded = cls.encode_base32(random_number, 16)

        # Combine the two parts to form the ULID
        return timestamp_encoded + randomness_encoded


# Define a custom SQLAlchemy type to handle ULIDs
class ULIDType(TypeDecorator):
    """Custom SQLAlchemy type for ULID."""

    impl = CHAR(26)  # ULIDs are 26 characters long

    def process_bind_param(self, value, dialect):
        # Ensure value is a 26-character ULID string when stored in the database
        if isinstance(value, str) and len(value) == 26:
            return value
        elif value is None:
            return None
        else:
            raise ValueError("Invalid ULID format")

    def process_result_value(self, value, dialect):
        # Return the ULID string as-is when retrieved
        return value
