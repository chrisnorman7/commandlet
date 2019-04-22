import re
from pytest import raises

from commandlet import Command
from commandlet.exc import InvalidFilterError, UnusedArgumentError


match_result = object()


class MatchFailed(Exception):
    pass


class PretendPlayer:
    match_string = 'test_match'

    def match(self, text):
        if text == self.match_string:
            return match_result
        raise MatchFailed(text)


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
    assert cmd.regexp is re.compile('^%s$' % name)
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


def test_to_int(parser):
    @parser.command('convert', 'convert <int:number>')
    def do_convert(number):
        return number

    n = 12345
    string = str(n)
    assert parser.commands[0].call(number=string) == n


def test_to_float(parser):
    @parser.command('convert', 'convert <float:number>')
    def do_convert(number):
        return number

    string = '3.141793'
    f = float(string)
    assert parser.commands[0].call(number=string) == f


def test_multiple_args(parser):
    @parser.filter('obj')
    def do_match(text, player):
        return player.match(text)

    @parser.command('match', 'match <obj:obj>')
    def match_command(obj):
        return match_result

    player = PretendPlayer()
    cmd = parser.commands[0]
    assert cmd.call(obj=player.match_string, player=player) is match_result
    string = 'willfail'
    with raises(MatchFailed) as exc:
        cmd.call(obj=string, player=player)
    assert exc.value.args == (string,)


def test_keyword_arguments(parser):

    @parser.command('test', 'test', 'test <hello>')
    def do_test(hello='world'):
        return hello

    assert parser.handle_command('test') == 'world'
    assert parser.handle_command('test this') == 'this'
