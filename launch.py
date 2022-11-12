from functools import reduce
from pprint import pprint

from interpreter.program import Program


if __name__ == '__main__':

    # p = Program('./examples/first.mo')
    # p = Program('./tests/example.mo')
    # p = Program('./tests/example_2.mo')
    p = Program('./tests/example_3.mo')
    p.run()