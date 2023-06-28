from typing import Callable, Optional
from functools import wraps


def format_args(obj: Optional[Callable]) -> Optional[dict]:
    """Format the arguments of the given object.

    Args:
        obj: The object to format the arguments for.

    Returns:
        A dictonary containing the formatted arguments
        of the given object. Or None if no valid object was given.
    """

    if isinstance(obj, object):
        return dict(
            zip(obj.__dict__.keys(), map(lambda x: str(x), obj.__dict__.values()))
        )

# def debug_log() -> Callable:

#     def wrapper