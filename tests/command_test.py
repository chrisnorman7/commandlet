import re
from pytest import raises

from commandlet import Command
from commandlet.exc import InvalidFilterError, UnusedArgumentError


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


def test_invalid_filter(parser):
    with raises(InvalidFilterError) as exc:
        parser.command('test', 'test <invalid:text>')(lambda text: print(text))
    cmd, name = exc.value.args
    assert isinstance(cmd, Command)
    assert name == 'invalid'


def test_unused_argument(parser):
    with raises(UnusedArgumentError) as exc:
        parser.command('test', 'test <text>')(lambda: print('Failed.'))
    cmd, name = exc.value.args
    assert isinstance(cmd, Command)
    assert name == 'text'


def test_call(parser):
    @parser.command('test', 'test <first> with <second>')
    def do_test(first, second):
        return first, second

    first = 'hello'
    second = 'world'
    f, s = parser.commands[0].call(first=first, second=second)
    assert f == first
    assert s == second
