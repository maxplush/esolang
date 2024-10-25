'''
>>> tree = parser.parse("")
>>> tree = parser.parse(";")
>>> tree = parser.parse(";;;;")
>>> tree = parser.parse("{{}}")
>>> tree = parser.parse(";{};{;;}")
>>> tree = parser.parse(";{{}{{}}};{;{}{;};}")
'''

import lark


grammar = r"""
    ?start: start (";" start)*
        | block
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


class _Eval(lark.Transformer):
    def start(self, xs):
        if len(xs) > 0:
            return xs[-1]
        else:
            None

    def block(self, xs):
        return xs[-1]
        
