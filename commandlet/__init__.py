"""Commandlet. Used for making Werkzeug-style commands without all the WSGI
stuff."""

from .commands import Argument, Command, CommandFunction
from .filters import Filter
from .parser import Parser, command

__all__ = []

for thing in (Argument, Command, CommandFunction, Filter, Parser, command):
    __all__.append(thing.__name__)
