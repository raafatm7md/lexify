from lexer import *
from parser import *
from symbol_table import *

if __name__ == '__main__':
    # Read the source code from the file
    with open('code.txt', 'r') as file:
        source_code = file.read()

    # Tokenize the source code
    tokens = lexer(source_code)

    # Parse the tokens to generate the parse tree
    parse_tree = parse_program(tokens)

    # Print the parse tree
    print_tree(parse_tree)

    # Create a symbol table and parse the code to populate it
    symbol_table = SymbolTable()
    symbol_table.parse_code(source_code)

    # Display the symbol table
    symbol_table.display_table()
