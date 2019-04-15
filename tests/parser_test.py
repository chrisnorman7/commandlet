from re import Pattern

from pytest import raises

from commandlet import Parser, Filter
from commandlet.exc import ConvertionError


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