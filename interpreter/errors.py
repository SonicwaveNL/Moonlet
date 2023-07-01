from typing import Optional
from interpreter.position import Position


class Error:
    """Default base Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        self.details = details
        self.pos = pos

    def __str__(self):
        return f"{self.__class__.__name__}: {self.details}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(details='{self.details!r}', pos={self.pos!r})"
        )


class InvalidSyntaxError(Error):
    """Invalid Syntax Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        super().__init__(details, pos)


class NotImplementedError(Error):
    """Default base Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        super().__init__(details, pos)


class RunTimeError(Error):
    """Default base Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        super().__init__(details, pos)


class ZeroDivisionError(Error):
    """Default base Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        super().__init__(details, pos)


class FileNotFoundError(Error):
    """Default base Error.

    Attributes:
        details: Detail description of the Error message.
        pos: Optional Position where the Error occured.
    """

    def __init__(self, details: Optional[str] = "", pos: Optional[Position] = ""):
        """Initialise the error with the details and optional Position.

        Args:
            details: Detail description of the Error message. Defaults to ''.
            pos: Optional Position where the Error occured. Defaults to ''.
        """
        super().__init__(details, pos)
