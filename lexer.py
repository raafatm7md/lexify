import re
from tabulate import tabulate


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type


keywords = ['if', 'else', 'while', 'int', 'float', 'char', 'return', 'print']
token_re = [
        (r'[_a-zA-Z][_a-zA-Z0-9]*', 'IDENTIFIER'),
        (r'\d+(\.\d+)?', 'CONSTANT'),
        (r'\'[^\']*\'|\"[^\"]*\"', 'STRING'),
        (r'[(){};,]', 'PUNCTUATION'),
        (r'[\[\]]', 'BRACKET'),
        (r'[+\-*/^%]', 'OPERATOR'),
        (r'=', 'ASSIGNMENT'),
        (r'==|!=|<=|>=|<|>', 'COMPARISON'),
    ]
comment_re = r'//.*?$'


def lexer(program):
    program = re.sub(comment_re, '', program, flags=re.MULTILINE)
    tokens = []
    tokens_print = []

    i = 0
    while i < len(program):
        match = None
        for token in token_re:
            pattern, name = token
            regex = re.compile(pattern)
            match = regex.match(program, i)
            if match:
                text = match.group()
                if name == 'IDENTIFIER' and text in keywords:
                    name = 'KEYWORD'
                tokens.append(Token(text, name))
                tokens_print.append([text, name])
                i = match.end()
                break
        if not match:
            if program[i].isspace():
                i += 1
            else:
                raise SyntaxError(f'Illegal character: {program[i]}')
    print('--------------------------')
    print(tabulate(tokens_print, headers=['Lexeme', 'Token'], tablefmt='github'))
    print('--------------------------')
    print(f'total number of tokens: {len(tokens_print)}\n')
    return tokens
