from lexer import *
from parser import *
from symbol_table import *

if __name__ == '__main__':
    source_code = open('code.txt', 'r').read()
    tokens = lexer(source_code)
    symbol_table = SymbolTable()
    symbol_table.parse_code(source_code)
    symbol_table.display_table()
