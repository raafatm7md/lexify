import re
import sys


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert_tree(root, key):
    if root is None:
        return Node(key)
    if root.val < key:
        root.right = insert_tree(root.right, key)
    else:
        root.left = insert_tree(root.left, key)
    return root


def print_symbol_tree(root):
    if root is None:
        return
    queue = [root]
    while queue:
        level_length = len(queue)
        for _ in range(level_length):
            node = queue.pop(0)
            print(node.val, end="")
            if node.left:
                queue.append(node.left)
                print(" L", end="")
            if node.right:
                queue.append(node.right)
                print(" R", end="")
            print("  ", end="")
        print()


class Symbol:
    def __init__(self, counter, name, obj_address, variable_type, dimension, line_declaration):
        self.counter = counter
        self.name = name
        self.obj_address = obj_address
        self.variable_type = variable_type
        self.dimension = dimension
        self.line_declaration = line_declaration
        self.line_reference = []

    def add_reference(self, line_reference):
        self.line_reference.append(line_reference)


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.symbol_names = []
        self.counter = 1
        self.errors = {}

    def add_variable(self, name, obj_address, variable_type, dimension, line_declaration):
        if name not in self.symbols:
            self.symbols[name] = Symbol(self.counter, name, obj_address, variable_type, dimension, line_declaration)
            self.counter += 1
            self.symbol_names.append(name)

    def add_reference(self, name, line_reference):
        if name in self.symbols:
            if line_reference not in self.symbols[name].line_reference and line_reference != self.symbols[name].line_declaration:
                self.symbols[name].add_reference(line_reference)
        else:
            cleaned_name = re.sub(r'\b(int|float|char|bool)\b', ' ', name).strip()
            if cleaned_name:
                self.errors[cleaned_name] = line_reference

    def parse_code(self, code):
        lines = code.split('\n')
        for current_line, line in enumerate(lines, 1):
            match = re.match(r'^\s*(int|float|char|bool)\s+([a-zA-Z_]\w*)(\s*\[\d+\])*(\s*\[\d+\])*', line)
            if match:
                variable_type = match.group(1)
                variable_name = match.group(2)
                obj_address = hex(id(variable_name))
                dimension = line.count('[')
                self.add_variable(variable_name, obj_address, variable_type, dimension, current_line)

            references = re.findall(r'\b([a-zA-Z_]\w*)\b(?!\s*=\s*;)', re.sub(r'\'[^\']*\'|\"[^\"]*\"', '', line))
            for reference in references:
                self.add_reference(reference.strip(), current_line)

    def display_table(self):
        print("\nSymbol Table:")
        print("{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format('Counter', 'Variable Name', 'Obj Address', 'Type', 'Dimension', 'Line Declaration', 'Line Reference'))
        for symbol in self.symbols.values():
            print("{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format(symbol.counter, symbol.name, symbol.obj_address, symbol.variable_type, symbol.dimension, symbol.line_declaration, ', '.join(map(str, symbol.line_reference))))

        for name, line in self.errors.items():
            print(f'\nError: Undeclared variable __{name}__ in line {line}', file=sys.stderr)

        for symbol in self.symbols.values():
            if not symbol.line_reference:
                print(f'Warning: Unused variable __{symbol.name}__ declared in line {symbol.line_declaration}', file=sys.stderr)

        ordered_symbols = sorted(self.symbol_names)
        print(f'\nUnordered: {" ".join(self.symbol_names)}')
        print(f'Ordered: {" ".join(ordered_symbols)}\n')

        for symbol in self.symbol_names:
            print(f'hash({symbol}) = ({len(symbol)} + {ord(symbol[0])}) % {self.counter - 1} = {(len(symbol) + ord(symbol[0])) % (self.counter - 1)}')

        root = Node(self.symbol_names[0])
        for name in self.symbol_names[1:]:
            insert_tree(root, name)
        print()
        print_symbol_tree(root)
