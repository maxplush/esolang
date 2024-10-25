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


class Simplifier(esolang.Arithmetic.Simplifier):
    '''
    >>> simplifier = Simplifier()
    >>> simplifier.transform(parser.parse("a = 2"))
    2
    >>> simplifier.transform(parser.parse("a"))
    2
    >>> simplifier.transform(parser.parse("a + 2"))
    4
    >>> simplifier.transform(parser.parse("b = 2"))
    2
    '''
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
