import readline
import esolang.Arithmetic
import esolang.Base
import esolang.Variables


def run_repl(lang = esolang.Variables):
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
    run_repl()
