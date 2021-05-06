from interpreter.lexer import Lexer

from pprint import pprint


if __name__ == '__main__':

    file_location = './examples/first.mo'
    file = open(file_location, 'r')

    print('\nFILE')
    print('==============')
    file_lines = file.read()
    print(file_lines)

    lexer = Lexer(file_lines)

    print('\nLINES')
    print('==============')
    lines = lexer.convert_to_lines(file_lines)
    pprint(lines)

    print('\nMAPPED PARTS')
    print('==============')
    mapped_parts = list(map(lexer.convert_to_parts, lines))
    pprint(mapped_parts)

    print('\nTO TOKENS')
    print('==============')
    found_tokens = list(map(lexer.convert_to_tokens, mapped_parts))
    pprint(found_tokens)

    print('\nTOKEN TYPES')
    print('==============')
    print(lexer.token_types)