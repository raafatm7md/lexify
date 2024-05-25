import re
from tabulate import tabulate


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type


# Define keywords and token patterns
keywords = {'if', 'else', 'while', 'int', 'float', 'char', 'return', 'print'}
token_patterns = [
    (r'[_a-zA-Z][_a-zA-Z0-9]*', 'IDENTIFIER'),
    (r'\d+(\.\d+)?', 'CONSTANT'),
    (r'\'[^\']*\'|\"[^\"]*\"', 'STRING'),
    (r'[(){};,]', 'PUNCTUATION'),
    (r'[\[\]]', 'BRACKET'),
    (r'[+\-*/^%]', 'OPERATOR'),
    (r'=', 'ASSIGNMENT'),
    (r'==|!=|<=|>=|<|>', 'COMPARISON'),
]
comment_pattern = r'//.*?$'


def lexer(program):
    # Remove comments
    program = re.sub(comment_pattern, '', program, flags=re.MULTILINE)

    tokens = []
    tokens_print = []
    i = 0

    while i < len(program):
        if program[i].isspace():
            i += 1
            continue

        match = None
        for pattern, name in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(program, i)
            if match:
                lexeme = match.group()
                if name == 'IDENTIFIER' and lexeme in keywords:
                    name = 'KEYWORD'
                tokens.append(Token(lexeme, name))
                tokens_print.append([lexeme, name])
                i = match.end()
                break

        if not match:
            raise SyntaxError(f'Illegal character: {program[i]}')

    # Display token information
    print('--------------------------')
    print(tabulate(tokens_print, headers=['Lexeme', 'Token'], tablefmt='fancy_grid'))
    print(f'Total number of tokens: {len(tokens_print)}')
    print('--------------------------\n')

    return tokens
