from pytest import fixture

from commandlet import Parser


@fixture(name='parser')
def get_parser():
    return Parser()
