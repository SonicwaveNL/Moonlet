import os
from argparse import ArgumentParser
from interpreter.launcher import Launcher
from interpreter.errors import FileNotFoundError

if __name__ == '__main__':

    # Define the Arguments Parser and it's arguments
    parser = ArgumentParser(prog='Moonlet', description='Moonlet programming interpreter language')
    parser.add_argument('file_input', nargs='?', default=os.getcwd())
    parser.add_argument('-f', '--file', metavar='file_path', type=str, help="Path to a '.mnl' file.")
    parser.add_argument('-d', '--debug', default=False, action="store_true", help="Execute code with DEBUG mode enabled.")
    parser.add_argument('-t', '--test', default=False, action="store_true", help="Run all Testing functions.")
    args = parser.parse_args()

    # Store the result of the parser in named variables
    file_path = args.file_input if args.file_input is not None else args.file_path
    debug_mode = args.debug
    test_mode = args.test

    print(f"{'MOONLET':=^60}")
    print(f"{'FILE_PATH:': <20} {file_path}")
    print(f"{'DEBUG:': <20} {debug_mode}")
    print(f"{'TEST:': <20} {test_mode}")

    launcher = Launcher(file_path=file_path)