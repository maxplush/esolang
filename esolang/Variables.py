import lark
import esolang.Arithmetic


grammar = esolang.Arithmetic.grammar + r"""
    %extend start: assign_var

    assign_var: NAME "=" sum

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

    %extend atom: NAME -> access_var
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.Arithmetic.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a = 2"))
    2
    >>> interpreter.visit(parser.parse("a + 2"))
    4
    >>> interpreter.visit(parser.parse("a = a + 3"))
    5
    >>> interpreter.visit(parser.parse("b = 3"))
    3
    >>> interpreter.visit(parser.parse("a * b"))
    15
    '''
    def __init__(self):
        self.locals = {}

    def assign_var(self, tree):
        name = tree.children[0].value
        value = self.visit(tree.children[1])
        self.locals[name] = value
        return value

    def access_var(self, tree):
        name = tree.children[0].value
        return self.locals[name]


class _Eval(esolang.Arithmetic._Eval):
    def __init__(self):
        self.locals = {}

    def assign_var(self, xs):
        name = xs[0]
        value = xs[1]
        self.locals[name] = value
        return value

    def access_var(self, xs):
        name = xs[0]
        return self.locals[name]


_state = _Eval()

def eval(expr):
    '''
    >>> eval("a = 2")
    2
    >>> eval("a")
    2
    >>> eval("a + 2")
    4
    >>> eval("b = 2")
    2
    '''
    tree = parser.parse(expr)
    return _state.transform(tree)
