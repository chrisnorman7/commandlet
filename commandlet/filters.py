"""Provides the Filter class."""

from attr import attrs, attrib

from .commands import CommandFunction


@attrs
class FilterBase:
    """Add name and replacement arguments."""

    name = attrib()
    replacement = attrib()


@attrs
class Filter(FilterBase, CommandFunction):
    """A filter for use with command parsers."""

    def call(self, **context):
        """Call this command, extracting argument values from context."""
        args = self.make_args(**context)
        return self.func(*args)
