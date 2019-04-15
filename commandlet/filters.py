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
