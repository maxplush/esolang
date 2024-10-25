import lark
import esolang.Arithmetic
import esolang.Variables


grammar = esolang.Variables.grammar + r"""
    %extend start: forloop

    forloop: "for" NAME "in" range block

    range: "range" "(" NUMBER ")"
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.Variables.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    '''
    def range(self, tree):
        return range(int(tree.children[0].value))

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])
        for x in xs:
            self.locals[varname] = x
            result = self.visit(tree.children[2])
        return result
