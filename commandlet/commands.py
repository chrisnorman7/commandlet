"""Provides the Command and Argument classes."""

import re
from inspect import signature

from attr import attrs, attrib, Factory

from .exc import InvalidFilterError, UnusedArgumentError


@attrs
class CommandFunction:
    """The very base of filters. Also used by commands."""

    func = attrib()
    args = attrib(default=Factory(list), init=False)
    defaults = attrib(default=Factory(dict), init=False)

    def __attrs_post_init__(self) -> None:
        s = signature(self.func)
        for p in s.parameters.values():
            if p.kind is not p.POSITIONAL_ONLY:
                self.defaults[p.name] = p.default
            self.args.append(p.name)

    def make_args(self, **context):
        """Returns a list of arguments whose values are extracted from context,
        and are in the order specified by self.args."""
        return [context.get(arg, self.defaults[arg]) for arg in self.args]


@attrs
class Argument:
    """A command argument. Basically just a name and a filter."""

    name = attrib()
    filter = attrib()


@attrs
class Command:
    """A command which has been decorated with Parser.command."""

    parser = attrib(repr=False)
    name = attrib()
    usage = attrib()
    func = attrib()
    regexp = attrib(default=Factory(type(None)), init=False)
    args = attrib(default=Factory(list), init=False)

    def __attrs_post_init__(self):
        self.func = CommandFunction(self.func)
        self.regexp = re.sub(
            self.parser.command_argument_regexp, self.convert_argument,
            self.usage
        )
        self.regexp = '^%s$' % self.regexp
        self.regexp = re.compile(self.regexp)

    def convert_argument(self, match):
        """Convert an argument to a regular expression, and update
        self.arguments."""
        full, string = match.groups()
        data = string.split(':', 1)
        if len(data) == 1:
            data.insert(0, self.parser.default_command_argument_filter)
        filter_name, argument_name = data
        filter_name = filter_name.strip()
        argument_name = argument_name.strip()
        if argument_name not in self.func.args:
            raise UnusedArgumentError(self, argument_name)
        try:
            f = self.parser.filters[filter_name]
        except KeyError:
            raise InvalidFilterError(self, filter_name)
        self.args.append(Argument(argument_name, f))
        return '(?P<%s>%s)' % (argument_name, f.replacement)

    def make_args(self, **context):
        """Make a list of arguments which can be passed to self.call."""
        for arg in self.args:
            name = arg.name
            text = context[name]
            value = arg.filter.call(text=text, **context)
            context[name] = value
        return self.func.make_args(**context)

    def call(self, **context):
        """Call this command, extracting argument values from context."""
        args = self.make_args(**context)
        return self.func.func(*args)
