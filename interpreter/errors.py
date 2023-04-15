from typing import Optional
from .position import Position

class Error:

    def __init__(self, type: Optional[str] = 'BaseError', details: Optional[str] = '', pos: Optional[Position] = None):
        self.type = type
        self.details = details
        self.pos = pos

    def __str__(self):
        return f"Error(type='{self.type}', details='{self.details}', pos={self.pos})"
    
    def __repr__(self):
        return f"Error(type='{self.type}', details='{self.details}', pos={self.pos})"

class InvalidSyntaxError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = None):
        super().__init__('InvalidSyntaxError', details, pos)

class UnknownCharError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = None):
        super().__init__('UnknownCharacterError', details, pos)

class NotImplementedError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = None):
        super().__init__('NotImplementedError', details, pos)

class RunTimeError(Error):
    def __init__(self, details: Optional[str] = '', pos: Optional[Position] = None):
        super().__init__('RunTimeError', details, pos)