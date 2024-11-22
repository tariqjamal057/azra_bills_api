"""Module containing custom exception classes."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pydantic_core import InitErrorDetails


class HTTPNotFoundException(HTTPException):
    """Exception raised when a requested resource is not found.

    Extends HTTPException to return a 404 status code.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize the HTTPNotFoundException.

        Args:
            detail: Additional details about the exception.
            headers: Optional dictionary of headers to include in the response.
        """
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail, headers)


class InternalServerErrorException(HTTPException):
    """Exception raised for internal server errors.

    Extends HTTPException to return a 500 status code.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize the InternalServerErrorException.

        Args:
            detail: Additional details about the exception.
            headers: Optional dictionary of headers to include in the response.
        """
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, detail, headers)


class FileNotFoundException(HTTPException):
    """Exception raised when a requested file is not found.

    Extends HTTPException to return a 404 status code.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize the FileNotFoundException.

        Args:
            detail: Additional details about the exception.
            headers: Optional dictionary of headers to include in the response.
        """
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail, headers)


class ForbiddenError(HTTPException):
    """Exception raised when access to a resource is forbidden.

    Extends HTTPException to return a 403 status code.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        """Initialize the ForbiddenError.

        Args:
            detail: Additional details about the exception.
            headers: Optional dictionary of headers to include in the response.
        """
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail, headers)


class HTTPForbiddenError(JSONResponse):
    """Exception raised for forbidden requests.

    Extends JSONResponse to return a 403 Forbidden response.

    Args:
        detail: Additional details about the exception.
        headers: Optional dictionary of headers to include in the response.
    """

    def __init__(self, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(
            status_code=status_code,
            content={
                "detail": detail,
            },
            headers=headers,
        )


class BadRequestError(JSONResponse):
    """Exception return for bad requests.

    Extends JSONResponse to return a 400 Bad Request response.

    Args:
        detail: Additional details about the exception.
        headers: Optional dictionary of headers to include in the response.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(
            status_code=status_code,
            content={
                "detail": detail,
            },
            headers=headers,
        )


class CustomPydanticValidationError(JSONResponse):
    """Custom Pydantic validation error response.

    Formats validation errors in Pydantic error response style.
    """

    def __init__(
        self,
        error_details: List[dict],
    ) -> None:
        """Initialize the CustomPydanticValidationError.

        Args:
           error_details: List of dictionaries containing error details.
        """
        validation_errors = []
        for error in error_details:
            if isinstance(error["value"], datetime):
                error["value"] = error["value"].strftime("%Y-%m-%d %H:%M:%S")
            error_detail = InitErrorDetails(
                {
                    "type": "value_error",
                    "loc": ["body"] + error.get("path", []) + [error["field"]],
                    "input": error["value"],
                    "ctx": {"error": error["message"]},
                }
            )
            validation_errors.append(error_detail)
        pydantic_error = ValidationError.from_exception_data(
            title="integrity_error", line_errors=validation_errors
        )
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": pydantic_error.errors()},
        )


class CustomPydanticMissingError(JSONResponse):
    """Custom Pydantic missing field error response.

    Formats missing field errors in Pydantic error response style.
    """

    def __init__(
        self,
        error_details: List[dict],
    ) -> None:
        """Initialize the CustomPydanticMissingError.

        Args:
           error_details: List of dictionaries containing error details.
        """
        missing_errors = []
        for error in error_details:
            error_detail = InitErrorDetails(
                {
                    "type": "missing",
                    "loc": ("body", error["field"]),
                    "input": {},
                }
            )
            missing_errors.append(error_detail)
        pydantic_error = ValidationError.from_exception_data(
            title="missing_error", line_errors=missing_errors
        )
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": pydantic_error.errors()},
        )


class HTTPNotFoundError(JSONResponse):
    """Exception return when a requested resource is not found.

    Extends JSONResponse to return a 404 Not Found HTTP response.

    Args:
        detail: Additional details about the error.
        headers: Optional dictionary of headers to include in the response.
    """

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(
            status_code=status_code,
            content={
                "detail": detail,
            },
            headers=headers,
        )
