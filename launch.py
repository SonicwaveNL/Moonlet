from functools import reduce
from pprint import pprint

from interpreter.launcher import Launcher


if __name__ == '__main__':

    # p = Program('./examples/first.mo')
    # p = Program('./tests/example_1.mo')
    # p = Program('./tests/example_2.mo')
    # p = Program('./tests/example_3.mo')
    # p = Program('./tests/example_4.mo')
    p = Launcher('./tests/base.mo')
    p.run()