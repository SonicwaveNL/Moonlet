from typing import Optional

class Position:

    def __init__(self, line: int = 0, start: int = 0, end: Optional[int] = None):
        self.line = line
        self.start = start
        self.end = start if end is None else end

    def __str__(self) -> str:
        return f"Pos(line={self.line}, start={self.start}, end={self.end})"
    
    def __repr__(self) -> str:
        return f"Pos(line={self.line}, start={self.start}, end={self.end})"
    
    def next(self, steps: Optional[int] = 1):
        self.start += steps
        self.end = self.start

    def nextl(self):
        self.line += 1
        self.start, self.end = 0, 0
    
    def copy(self, steps: Optional[int] = 0):
        return Position(self.line, self.start, self.end + steps if steps > 0 else self.end)