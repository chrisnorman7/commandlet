import re
from pytest import raises

from commandlet import Command


class Works(Exception):
    pass


def test_blank(parser):
    name = 'test'

    @parser.command(name)
    def do_test():
        raise Works()

    cmd = parser.commands[0]
    assert cmd.name == name
    assert cmd.usage == name
    assert isinstance(cmd, Command)
    assert cmd.regexp is re.compile(name)
    assert parser.commands == [cmd]
    assert cmd.func.func is do_test


def test_with_args(parser):
    name = 'test'

    @parser.command(name, '%s <text>' % name)
    def do_test(text):
        return text

    cmd = parser.commands[0]
    assert cmd.func.args == ['text']
