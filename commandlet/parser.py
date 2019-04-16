"""Provides the Parser class."""

import re
from attr import attrs, attrib, Factory

from .commands import Command
from .exc import ConvertionError
from .filters import Filter


@attrs
class Parser:
    """A command parser. Decorate commands with Parser.command, filters with
    Parser.filter, and handle commands with Parser.handle_command."""

    commands = attrib(default=Factory(list), init=False)
    filters = attrib(default=Factory(dict))
    default_command_argument_filter = attrib(default=Factory(lambda: 'str'))
    command_argument_regexp = attrib(
        default=Factory(lambda: re.compile('(<([^>]+)>)'))
    )

    def __attrs_post_init__(self):
        self.filter('str')(lambda text: text)
        self.filter('int', replacement='[0-9]+')(self.to_int)
        self.filter('float', replacement='[0-9]+[.][0-9]+')(self.to_float)

    def to_int(self, text):
        """Convert text to an integer."""
        try:
            return int(text)
        except ValueError:
            raise ConvertionError('Could not convert %r t an integer.' % text)

    def to_float(self, text):
        """Convert text to a float."""
        try:
            return float(text)
        except ValueError:
            raise ConvertionError('Could not convert %r t a float.' % text)

    def filter(self, name, replacement='.+'):
        """Decorate a function to be used as a filter. The function should take
        an argument named "text" if it wants to get the text that it is
        supposed to check."""
        def inner(func):
            self.filters[name] = Filter(name, replacement, func)
            return func
        return inner

    def command(self, name, *formats):
        """A decorator to add a command. You must provide a name, then at least
        one format which can be used to invoke the command."""

        def inner(func):
            _formats = formats
            if not _formats:
                _formats = [name]
            for format in _formats:
                self.commands.append(Command(self, name, format, func))
            return func

        return inner
