import lark
import esolang.level1_statements

grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop | whileloop | whileloop | range | comparison

    forloop: "for" NAME "in" range block
    whileloop: "while" comparison block
    range: "range" "(" start ")"
    comparison: start COMPARISON_OPERATOR start
    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined

    >>> interpreter.visit(parser.parse("a=5; for i in range(a) {a = a + i}; a"))
    15
    >>> interpreter.visit(parser.parse("a=0; while a < 10 {a = a + 1}"))
    10
    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 1}; a"))
    5
    >>> interpreter.visit(parser.parse("1 > 0"))
    0
    >>> interpreter.visit(parser.parse("0 > 1"))
    1

    >>> interpreter.visit(parser.parse("a=0; while a < 6 {a = a + 1}; a"))
    6

    >>> interpreter.visit(parser.parse("a=0; while a < 7 {a = a + 3}; a"))
    9

    >>> interpreter.visit(parser.parse("a=10; while a > 0 {a = a - 2}; a"))
    0

    >>> interpreter.visit(parser.parse("a=1; while a < 4 {a = a * 2}; a"))
    4

    >>> interpreter.visit(parser.parse("a=0; for i in range(3) {a = a + i}; a"))
    3

    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 2}; a"))
    6
    
    >>> interpreter.visit(parser.parse("a=0; while a < 10 {a = a + 3}; a"))
    12

    >>> interpreter.visit(parser.parse("a=5; while a > 3 {a = a - 1}; a"))
    3

    >>> interpreter.visit(parser.parse("a=0; while a < 2 {a = a + 1}; a"))
    2
    '''
    def range(self, tree):
        return range(int(self.visit(tree.children[0])))

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])
        self.stack.append({})
        for x in xs:
            self.stack[-1][varname] = x
            result = self.visit(tree.children[2])
        self.stack.pop()
        return result
    def whileloop(self, tree):
        while self.visit(tree.children[0]) == 0:
            a = self.visit(tree.children[1])
        return a
    def comparison(self, tree):
        v1 = self.visit(tree.children[0])
        op = tree.children[1].value
        v2 = self.visit(tree.children[2])
        if eval(str(v1) + op + str(v2)):
            return 0
        else:
            return 1
        pass
    
interpreter = Interpreter()
interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 1}; a"))