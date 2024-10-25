import readline
import esolang.Arithmetic
import esolang.Base
import esolang.Variables
import esolang.For
import esolang.FunctionApplication


def run_repl(lang = esolang.For):
    parser = lang.parser
    interpreter = lang.Interpreter()
    while True:
        try:
            cmd = input('esolang> ')
            tree = parser.parse(cmd)
            result = interpreter.visit(tree)
            if result is not None:
                print(result)
        except EOFError:
            break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lang', default='For')
    args = parser.parse_args()

    run_repl()
