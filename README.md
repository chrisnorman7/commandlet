# commandlet
Workzeug-style commands.

## Usage
```
from commandlet.parser import Parser

p = Parser()


@p.command('test', 'test <int:times> <str:string>')
def do_test(times, string):
    """Test a certain number of times."""
    for n in range(times):
        print('[%d]: %s' % (n, string))


p.handle_command('test 4 Hello world.')
```

As you can see, you can decorate functions with the Parser.command decorator to make them callable. They should all be given a name (used for pretty-printing mainly), and an argument string, which looks very similar to those seen in command line programs... And [Workzeug](https://palletsprojects.com/p/werkzeug/).

You can also add extra filters:

```
@p.filter('reverse')
def do_reverse(text):
    return (text, ''.join(reversed(text)))


@p.command('reverse', 'reverse <reverse:string>')
def reverse_command(string):
    original, new = string
    print('Reversing %r gives %r.' % (original, new))
```

You can see the full list of filters by examining the Parser.filters dictionary. By default, str, int, and float are supported.
