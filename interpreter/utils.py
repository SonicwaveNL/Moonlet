from typing import Callable, Optional, List, Tuple, Union


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


def debug_log(category: Optional[str] = None, raw: bool = False) -> Callable:
    """Debug log decorator.

    Debug logger to print the params of a function,
    with the specified category (if provided).

    Args:
        category: Category name. Defaults to None.
        raw: Print Raw version.

    Returns:
        Returns the *args and **kwargs to continue the function.
    """

    def iter(items: Union[List, Tuple]) -> None:
        """Mini iterator function with printer.

        Iterate over items and print the content.

        Args:
            items: Items to iterate over.
        """
        # Stop if done with iterating
        if len(items) == 0:
            return

        # Return the last one, when only one is left
        elif len(items) == 1:
            return print(repr(items[0])) if raw else print(str(items[0]))

        # Go deeper when the current item is a list
        if isinstance(items[0], list):
            return iter(items[0])

        print(repr(items[0]), end=", ") if raw else print(str(items[0]), end=", ")
        return iter(items[1:])

    def wrapper(func: Callable) -> Callable:
        """Decorator wrapper.

        Args:
            func: Input function, who called the decorator.

        Returns:
            Function to be executed.
        """

        def inner(*args, **kwargs) -> Callable:
            """Decorator inner, who prints the category and it's arguments.

            Returns:
                Function to be executed with parameters.
            """
            debug_mode = False

            # Check if the input is a 'self'
            # param, so we can validate if
            # the input object has the 'debug_mode' attr
            if isinstance(args[0], object) and hasattr(args[0], "debug_mode"):
                debug_mode = args[0].debug_mode

            if debug_mode:
                if len(args[1:]) > 0:
                    print(f"{category: <30}", end=" ")
                    iter([*args[1:]])

                else:
                    print(f"{category: <30}")

            return func(*args, **kwargs)

        return inner

    return wrapper
