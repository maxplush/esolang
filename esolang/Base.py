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


grammar = r"""
    ?start: start (";" start)*
        | block
        | /#.*/                -> comment
        |

    block: "{" start* "}"
"""
parser = lark.Lark(grammar)


class Interpreter(lark.visitors.Interpreter):
    def start(self, tree):
        res = None
        for child in tree.children:
            res = self.visit(child)
        return res

    def block(self, tree):
        return self.visit(tree.children[0])


class Simplifier(lark.Transformer):
    def start(self, xs):
        if len(xs) > 0:
            return xs[-1]
        else:
            None

    def block(self, xs):
        return xs[-1]
        
