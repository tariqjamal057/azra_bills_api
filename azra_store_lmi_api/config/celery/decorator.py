"""Module contains decorator for running async tasks in Celery."""

from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

from asgiref import sync
from celery import Task

from azra_store_lmi_api.config.celery.app import celery

_P = ParamSpec("_P")
_R = TypeVar("_R")


def async_task(*args: Any, **kwargs: Any):
    """A decorator that converts an asynchronous function into a Celery task.

    This decorator allows you to easily transform asynchronous functions into
    Celery tasks, enabling them to be executed asynchronously within a Celery
    worker.

    Args:
        *args: Variable length argument list to be passed to the Celery task.
        **kwargs: Arbitrary keyword arguments to be passed to the Celery task.

    Returns:
        Callable: A decorator function that wraps the original asynchronous
        function and returns a Celery task.
    """

    def _decorator(func: Callable[_P, Coroutine[Any, Any, _R]]) -> Task:
        sync_call = sync.AsyncToSync(func)

        @celery.task(*args, **kwargs)
        @wraps(func)
        def _decorated(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            return sync_call(*args, **kwargs)

        return _decorated

    return _decorator
