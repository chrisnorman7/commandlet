from re import Pattern

from inspect import isgenerator

from pytest import raises

from commandlet import Parser, Filter, command, filter
from commandlet.exc import ConvertionError, CommandFailedError


class Works(Exception):
    pass


def test_init(parser):
    assert isinstance(parser, Parser)
    assert parser.commands == []
    assert isinstance(parser.filters, dict)
    assert parser.filters
    assert parser.default_command_argument_filter == 'str'
    assert isinstance(parser.command_argument_regexp, Pattern)


def test_filter(parser):

    @parser.filter('double')
    def do_double(text):
        return text * 2

    f = parser.filters['double']
    assert isinstance(f, Filter)
    assert f.func is do_double
    assert f.args == ['text']


def test_to_int(parser):
    assert parser.to_int('2') == 2
    assert parser.to_int('0') == 0
    with raises(ConvertionError):
        parser.to_int('one')
    assert isinstance(parser.to_int('1234'), int)


def test_to_float(parser):
    assert parser.to_float('4') == 4.0
    assert parser.to_float('0.0') == 0.0
    with raises(ConvertionError):
        parser.to_float('zero dot zero')
    assert isinstance(parser.to_float('0.5'), float)


def test_str_filter(parser):
    string = 'testing'
    assert parser.filters['str'].func(string) == string


def test_handle_command(parser):
    name = 'test'
    @parser.command(name, '%s <string>' % name)
    def do_test(string):
        return string

    string = 'this'
    assert parser.handle_command('%s %s' % (name, string)) == string


def test_command_failed(parser):
    @parser.command('test')
    def do_test():
        pass

    with raises(CommandFailedError) as exc:
        parser.handle_command('no such command')
    assert exc.value.tried_commands == []


def test_tried_commands(parser):
    name = 'convert'
    e = ConvertionError('Artificially cause command matching to fail.')

    @parser.command(name, '%s <number>' % name)
    def convert_1(number):
        raise e

    @parser.command(name, '%s <value>' % name)
    def convert_2(value):
        raise e

    with raises(CommandFailedError) as exc:
        parser.handle_command('%s %s' % (name, name))
    assert exc.value.tried_commands == parser.commands


def test_command():
    p1 = Parser()
    p2 = Parser()

    @command([p1, p2], 'test')
    def do_test():
        raise Works()

    with raises(Works):
        p1.handle_command('test')
    with raises(Works):
        p2.handle_command('test')


def test_generator(parser):

    @parser.command('test')
    def do_test():
        yield 1

    assert isgenerator(parser.handle_command('test'))


def test_copy(parser):
    parser.command('print')(lambda text: print(text))
    parser.command('nothing')(lambda: None)
    p = parser.copy()
    for a in parser.__attrs_attrs__:
        name = a.name
        old = getattr(parser, name)
        new = getattr(p, name)
        if old != new:
            raise RuntimeError(
                'Attribute %s does not match: %r -> %r.' % (name, old, new)
            )


def test__filter():
    p1 = Parser()
    p2 = Parser()

    @filter([p1, p2], 'test')
    def filter_test():
        pass

    assert 'test' in p1.filters
    assert 'test' in p2.filters
