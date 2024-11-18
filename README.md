# esolang ![](https://github.com/mikeizbicki/esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.

## New Level 0 Arithmetic Interpreter Doctest Examples

```python
>>> interpreter = Interpreter()
>>> interpreter.visit(parser.parse("if (0): { 10 } else 5"))  
5
>>> interpreter.visit(parser.parse("if (1): { 10 } else 5"))  
5
>>> interpreter.visit(parser.parse("a = 10; if (a): { 10 } else 0"))
0
>>> interpreter.visit(parser.parse("a = 1; if (a): { 10 } else 100"))
100
>>> interpreter.visit(parser.parse("x = 2; { x = x + 3; x + 5 }"))
10
>>> interpreter.visit(parser.parse("a=2; b=1; if (a-b): { 5 } else 1"))
1
```
## New Level 1 Interpreter Doctest Examples

```python
>>> interpreter = Interpreter()
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
>>> interpreter.visit(parser.parse("is_prime(5)"))
True
>>> interpreter.visit(parser.parse("is_prime(8)"))
False
```


