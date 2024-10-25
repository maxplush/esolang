import lark
import esolang.Base


grammar = esolang.Base.grammar + r"""
    %extend start: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
        | "(" sum ")"       -> paren

    NUMBER: /-?[0-9]+/

    %import common.WS_INLINE
    %ignore WS_INLINE
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.Base.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("1"))
    1
    >>> interpreter.visit(parser.parse("1+2"))
    3
    >>> interpreter.visit(parser.parse("1-2"))
    -1
    >>> interpreter.visit(parser.parse("(1+2)*3"))
    9
    >>> interpreter.visit(parser.parse("1+2*3"))
    7
    >>> interpreter.visit(parser.parse("1*2+3"))
    5
    >>> interpreter.visit(parser.parse("1*(2+3)"))
    5
    >>> interpreter.visit(parser.parse("(1*2)+3+4*(5-6)"))
    1
    '''
    def number(self, tree):
        return int(tree.children[0].value)

    def add(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 + v1

    def sub(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 - v1

    def mul(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 * v1

    def div(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 // v1

    def paren(self, tree):
        return self.visit(tree.children[0])


class _Eval(esolang.Base._Eval):
    def number(self, xs):
        return int(xs[0].value)

    def add(self, xs):
        return xs[0] + xs[1]

    def sub(self, xs):
        return xs[0] - xs[1]

    def mul(self, xs):
        return xs[0] * xs[1]

    def div(self, xs):
        return xs[0] // xs[1]

    def paren(self, xs):
        return xs[0]


def eval(expr):
    '''
    >>> eval("1")
    1
    >>> eval("1+2")
    3
    >>> eval("1-2")
    -1
    >>> eval("(1+2)*3")
    9
    >>> eval("1+2*3")
    7
    >>> eval("1*2+3")
    5
    >>> eval("1*(2+3)")
    5
    >>> eval("(1*2)+3+4*(5-6)")
    1
    '''
    tree = parser.parse(expr)
    return _Eval().transform(tree)


class _RemoveUnneededParentheses(lark.Transformer):
    def add(self, xs):
        for i in [0, 1]:
            if xs[i].data == 'paren':
                if xs[i].children[0].data in ['mul', 'div', 'add', 'sub']:
                    xs[i] = xs[i].children[0]
        return lark.Tree('add', xs)

    def sub(self, xs):
        for i in [0, 1]:
            if xs[i].data == 'paren':
                if xs[i].children[0].data in ['mul', 'div', 'add', 'sub']:
                    xs[i] = xs[i].children[0]
        return lark.Tree('sub', xs)

    def paren(self, xs):
        if xs[0].data in ['paren', 'number']:
            return xs[0]
        else:
            return lark.Tree('paren', xs)


class _TreeToString(lark.Transformer):
    def number(self, xs):
        return xs[0].value

    def start(self, xs):
        return xs[0]

    def add(self, xs):
        return xs[0] + "+" + xs[1]

    def sub(self, xs):
        return xs[0] + "-" + xs[1]

    def mul(self, xs):
        return xs[0] + "*" + xs[1]

    def div(self, xs):
        return xs[0] + "/" + xs[1]

    def paren(self, xs):
        return "(" + xs[0] + ")"


def minify(expr):
    '''
    >>> minify("1 + 2")
    '1+2'
    >>> minify("1 + ((((2))))")
    '1+2'
    >>> minify("1 + (2*3)")
    '1+2*3'
    >>> minify("1 + (2/3)")
    '1+2/3'
    >>> minify("(1 + 2)*3")
    '(1+2)*3'
    >>> minify("(1 - 2)*3")
    '(1-2)*3'
    >>> minify("(1 - 2)+3")
    '1-2+3'
    >>> minify("(1 + 2)+(3 + 4)")
    '1+2+3+4'
    '''
    tree = parser.parse(expr)
    tree = _RemoveUnneededParentheses().transform(tree)
    return _TreeToString().transform(tree)


def eval_rpn(expr):
    '''
    This function evaluates an expression written in RPN.

    RPN (Reverse Polish Notation) is an alternative syntax for arithmetic.
    It was widely used in the first scientific calculators because it is much easier to parse than standard infix notation.
    For example, parentheses are never needed to disambiguate order of operations.
    You can find more details on wikipedia: <https://en.wikipedia.org/wiki/Reverse_Polish_notation>.

    >>> eval_rpn("1")
    1
    >>> eval_rpn("1 2 +")
    3
    >>> eval_rpn("1 2 -")
    1
    >>> eval_rpn("1 2 + 3 *")
    9
    >>> eval_rpn("1 2 3 * +")
    7
    >>> eval_rpn("1 2 * 3 +")
    5
    >>> eval_rpn("1 2 3 + *")
    5
    >>> eval_rpn("1 2 * 3 + 4 5 6 - * +")
    9
    '''
    tokens = expr.split()
    stack = []
    operators = {
        '+': lambda a, b: a+b,
        '-': lambda a, b: a-b,
        '*': lambda a, b: a*b,
        '/': lambda a, b: a//b,
        }
    for token in tokens:
        if token not in operators.keys():
            stack.append(int(token))
        else:
            assert len(stack) >= 2
            v1 = stack.pop()
            v2 = stack.pop()
            stack.append(operators[token](v1, v2))
    assert len(stack) == 1
    return stack[0]


class _TreeToRPN(lark.Transformer):
    def number(self, xs):
        return xs[0].value

    def start(self, xs):
        return xs[0]

    def add(self, xs):
        return xs[0] + " " + xs[1] + " " + "+"

    def sub(self, xs):
        return xs[0] + " " + xs[1] + " " + "-"

    def mul(self, xs):
        return xs[0] + " " + xs[1] + " " + "*"

    def div(self, xs):
        return xs[0] + " " + xs[1] + " " + "/"

    def paren(self, xs):
        return xs[0]


def infix_to_rpn(expr):
    '''
    >>> infix_to_rpn('1')
    '1'
    >>> infix_to_rpn('1+2')
    '1 2 +'
    >>> infix_to_rpn('1-2')
    '1 2 -'
    >>> infix_to_rpn('(1+2)*3')
    '1 2 + 3 *'
    >>> infix_to_rpn('1+2*3')
    '1 2 3 * +'
    >>> infix_to_rpn('1*2+3')
    '1 2 * 3 +'
    >>> infix_to_rpn('1*(2+3)')
    '1 2 3 + *'
    >>> infix_to_rpn('(1*2)+3+4*(5-6)')
    '1 2 * 3 + 4 5 6 - * +'
    '''
    tree = parser.parse(expr)
    return _TreeToRPN().transform(tree)
