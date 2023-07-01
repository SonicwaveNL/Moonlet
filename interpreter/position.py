from typing import Optional


class Position:
    """Position of the Token.

    Representing the position of the Token within the input/file.

    Attributes:
        line: Line number.
        start: Start index.
        end: End index.
    """

    def __init__(self, line: int = 0, start: int = 0, end: Optional[int] = None):
        """Initializes the postion with given line and start to end index.

        Args:
            line: Line number. Defaults to 0.
            start: Start index. Defaults to 0.
            end: End index. Defaults to None.
        """
        self.line = line
        self.start = start
        self.end = start if end is None else end

    def __str__(self) -> str:
        if self.end is None:
            return f"{self.line} [{self.start}]"

        return f"{self.line} [{self.start}:{self.end}]"

    def __repr__(self) -> str:
        return f"Position(line={self.line!r}, start={self.start!r}, end={self.end!r})"

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Position):
            return False
        return self.line == rhs.line and self.start == rhs.start and self.end == rhs.end

    def next(self, steps: Optional[int] = 1):
        """Go to the next position.

        Args:
            steps: Step amount. Defaults to 1.
        """
        self.start += steps
        self.end = self.start

    def nextl(self):
        """Go to the next line."""
        self.line += 1
        self.start, self.end = 0, 0

    def copy(self, steps: Optional[int] = 0):
        """Return a copy of the Position.

        Args:
            steps: Extra steps to take from copied position. Defaults to 0.

        Returns:
            Copied position with optional made steps.
        """
        return Position(
            self.line, self.start, self.end + steps if steps > 0 else self.end
        )
