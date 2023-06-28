from interpreter.launcher import Launcher
from interpreter.utils import format_args
from interpreter.position import Position

if __name__ == '__main__':

    # p = Program('./examples/first.mnl')
    # p = Program('./tests/example_1.mnl')
    # p = Program('./tests/example_2.mnl')
    # p = Program('./tests/example_3.mnl')
    # p = Program('./tests/example_4.mnl')
    # p = Launcher('./tests/base.mnl')
    # p = Launcher('./tests/test_subroutine_1.mnl')
    # p = Launcher('./tests/test_subroutine_2.mnl')
    p = Launcher('./tests/test_subroutine_3.mnl')
    p.run()