'''

The following tests show example strings in the language.
There are no meaningful commands at this point,
only a block structure.

>>> tree = parser.parse("")
>>> tree = parser.parse(";")
>>> tree = parser.parse(";;;;")
>>> tree = parser.parse("{{}}")
>>> tree = parser.parse(";{};{;;}")
>>> tree = parser.parse(";{{}{{}}};{;{}{;};}")

The following tests check that unbalanced blocks correctly raise exceptions.

>>> tree = parser.parse("{") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{{}{}{{{}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{;;;}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedCharacters:
    
The following checks test that comments work.

>>> tree = parser.parse(";{};#")
>>> tree = parser.parse(";{};#{")
>>> tree = parser.parse(";{#}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

'''

import lark
import esolang.level0_arithmetic


grammar = esolang.level0_arithmetic.grammar + r"""
    %extend start: start (";" start)*
        | assign_var
        | block
        | /#.*/                -> comment
        | if_statement
        |
    # semantics
    # first start will run if condition is true
    # the second start if condition is F
    # sometimes called the "the ternerary operator"

    if_statement: condition "?" start ":" start

    # we wil not implment a boolean variable type
    # conditionals repersented as numbers

    condition: start 

    block: "{" start* "}"

    assign_var: NAME "=" start

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

    %extend atom: NAME -> access_var
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level0_arithmetic.Interpreter):
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
    >>> interpreter.visit(parser.parse("a = 3; {a+5}"))
    8
    >>> interpreter.visit(parser.parse("a = 3; {a=5; a+5}"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {a=5}; a+5"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {c=5}; c+5")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable c undefined
    '''
    def __init__(self):
        self.stack = [{}]

    def _get_from_stack(self, name):
        for d in reversed(self.stack):
            if name in d:
                return d[name]
        raise ValueError(f"Variable {name} undefined")

    def _assign_to_stack(self, name, value):
        for d in reversed(self.stack):
            if name in d:
                d[name] = value
                return value
        self.stack[-1][name] = value
        return value
    def if_statement(self, tree):
        import code; code.interact(local=locals())
        asd

    def assign_var(self, tree):
        name = tree.children[0].value
        value = self.visit(tree.children[1])
        self._assign_to_stack(name, value)
        return value

    def access_var(self, tree):
        name = tree.children[0].value
        return self._get_from_stack(name)

    def block(self, tree):
        self.stack.append({})
        res = self.visit(tree.children[0])
        self.stack.pop()
        return res
    
tree = parser.parse("1 ? 2 : 3")
# print(tree.pretty())  # Should now parse without errors

# interpreter = Interpreter()
# result = interpreter.visit(tree)
# print(result) 