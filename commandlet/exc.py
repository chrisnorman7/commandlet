"""Provides various Exception classes used by the library."""

from attr import attrs, attrib, Factory


class CommandletError(Exception):
    """The base exception class."""


class FilterError(CommandletError):
    """There was an error in the filtering system."""


class InvalidFilterError(FilterError):
    """No such filter found."""


class ConvertionError(FilterError):
    """There was an error while converting text using a filter."""


class CommandError(FilterError):
    """There is an error with a command."""


class UnusedArgumentError(CommandError):
    """The given argument is not named in the signature of the command
    function."""


class ParserError(CommandletError):
    """There was an error with the parser system."""


@attrs
class CommandFailedError(ParserError):
    """Handling of a command failed. Check the tried_commands attribute for a
    list of commands whose regular expressions were right, but not the content
    of the arguments."""

    tried_commands = attrib(default=Factory(list))
