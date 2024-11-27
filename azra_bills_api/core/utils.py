import os
import random
import string
import time
import uuid
from enum import Enum

from fastapi import Query
from fastapi_pagination import Params
from pydantic import field_validator


def uuid_generator():
    return str(uuid.uuid4())


class BaseEnum(Enum):
    """A base enumeration class that provides additional utility methods."""

    @property
    def name(self):
        """Returns the name of the enum member with underscores replaced by spaces and title-
        cased."""
        return self._name_.replace("_", " ").title()

    @classmethod
    def get_name_by_value(cls: type[Enum], value):
        """Returns the name of the enum member with the given value.

        Args:
            value: The value to search for.

        Returns:
            str: The name of the enum member if found, None otherwise.
        """
        for member in cls:
            if member.value == value:
                return member.name
        return None

    @classmethod
    def all(cls: type[Enum]):
        """Returns a list of dictionaries containing all enum members.

        Returns:
            list: A list of dictionaries with 'id' (value) and 'name' for each enum member.
        """
        return [{"id": member.value, "name": member.name} for member in cls]

    @classmethod
    def values(cls):
        """Returns a list of all enum member values.

        Returns:
            list: A list of all enum member values.
        """
        return [member.value for member in cls]

    @classmethod
    def names(cls):
        """Returns a list of all enum member names.

        Returns:
            list: A list of all enum member names.
        """
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


def generate_password(n: int = 12) -> str:
    """Generate a random password with specified length and character types.

    This function creates a password that includes at least one uppercase letter,
    one lowercase letter, one digit, and one special character. The remaining
    characters are randomly chosen from all character types.

    Args:
        n (int): The length of the password to generate. Defaults to 12.

    Returns:
        str: A randomly generated password of the specified length.
    """

    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation
    random_string = [
        random.choice(uppercase_chars),
        random.choice(lowercase_chars),
        random.choice(digits),
        random.choice(special_chars),
    ]
    all_chars = uppercase_chars + lowercase_chars + digits + special_chars
    random_string += [random.choice(all_chars) for _ in range(n - 4)]
    random.shuffle(random_string)
    return "".join(random_string)


class CustomParams(Params):
    """Custom parameters class extending Params.

    This class defines custom query parameters for pagination and filtering.

    Attributes:
        size (int): The number of items to return per page.
            Defaults to 10.
            Minimum value: 1
            Maximum value: 100
    """

    size: int = Query(default=10, ge=1, le=100, description="Page size")


class PhoneNumberValidator:
    """Validator for phone numbers."""

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")
        return value
