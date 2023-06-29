from argparse import ArgumentParser
from interpreter.launcher import Launcher

if __name__ == "__main__":
    # Define the Arguments Parser and it's arguments
    parser = ArgumentParser(
        prog="Moonlet", description="Moonlet programming interpreter language"
    )
    parser.add_argument("file_input", nargs="?", default="")
    parser.add_argument(
        "-f", "--file", metavar="file_path", type=str, help="Path to a '.mnl' file."
    )
    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        action="store_true",
        help="Execute code with DEBUG mode enabled.",
    )
    parser.add_argument(
        "-t",
        "--test",
        default=False,
        action="store_true",
        help="Run all Testing functions.",
    )
    args = parser.parse_args()

    # Store the result of the parser in named variables
    file_path = args.file_input if args.file_input is not None else args.file_path
    debug_mode = args.debug
    test_mode = args.test

    if debug_mode or test_mode:
        print(f"{'MOONLET':=^60}")
        print(f"{'FILE_PATH:': <30} {file_path}")
        print(f"{'DEBUG_MODE:': <30} {debug_mode}")
        print(f"{'TEST_MODE:': <30} {test_mode}")

    launcher = Launcher(file_path=file_path, debug_mode=debug_mode, test_mode=test_mode)
