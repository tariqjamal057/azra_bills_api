"""This module provides security-related functionality for password hashing and verification.

It includes a CryptContext for bcrypt hashing and an AuthenticationMixin class for handling
password-related operations.
"""

from typing import Union

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationMixin:
    """A mixin class that provides password hashing and verification functionality.

    This class is designed to be mixed into other classes that require
    password-related operations. It uses bcrypt for secure password hashing.

    Attributes:
        password (str): The hashed password. Defaults to None.

    Methods:
        get_hash_password(password_: str) -> str:
            Hashes the given password using bcrypt.
        verify_password(plain_password: str) -> Union[str, ValueError]:
            Verifies a plain password against the stored hashed password.
    """

    password = None

    def get_hash_password(self, password_: str) -> str:
        """Hash the given password using bcrypt.

        Args:
            password_ (str): The plain text password to be hashed.

        Returns:
            str: The bcrypt hash of the given password.
        """
        return bcrypt_context.hash(password_)

    def verify_password(self, plain_password: str) -> Union[str, ValueError]:
        """Verify a plain password against the stored hashed password.

        Args:
            plain_password (str): The plain text password to be verified.

        Returns:
            Union[str, ValueError]: True if the password is correct, False otherwise.
                                    Raises ValueError if no password is set.

        Raises:
            ValueError: If the password attribute is not set.
        """
        if self.password:
            return bcrypt_context.verify(plain_password, self.password)
        raise ValueError("Password is not set.")
