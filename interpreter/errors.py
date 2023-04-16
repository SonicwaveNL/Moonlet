from typing import Optional
from .position import Position

class Error:

    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        self.details = details
        self.pos = pos

    def __str__(self):
        return f"{self.__class__.__name__}: {self.details!r}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(details='{self.details!r}', pos={self.pos!r})"

class InvalidSyntaxError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        super().__init__(details, pos)

class UnknownCharError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        super().__init__(details, pos)

class NotImplementedError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        super().__init__(details, pos)

class RunTimeError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        super().__init__(details, pos)

class ZeroDivisionError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = ''):
        super().__init__(details, pos)