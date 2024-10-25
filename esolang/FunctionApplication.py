import lark
import esolang.Arithmetic
import esolang.Variables
import esolang.For


grammar = esolang.For.grammar + r"""
    %extend start: function

    lambda: "lambda" args_list ":" start

    ?args_list: start ("," start)*

    function: NAME "(" args_list ")"
        | NAME "(" ")"
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.For.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a=3; print(a)"))
    3
    >>> interpreter.visit(parser.parse("print(10)"))
    10
    >>> interpreter.visit(parser.parse("for i in range(10) {print(i)}"))
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    '''
    def __init__(self):
        super().__init__()
        self.locals['print'] = print

    def function(self, tree):
        name = tree.children[0]
        params = [self.visit(child) for child in tree.children[1:]]
        return self.locals[name](*params)
