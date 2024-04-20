import re
import sys


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
        self.counter = 1
        self.error = {}

    def add_variable(self, name, obj_address, variable_type, dimension, line_declaration):
        if name not in self.symbols:
            self.symbols[name] = Symbol(self.counter, name, obj_address, variable_type, dimension, line_declaration)
            self.counter += 1

    def add_reference(self, name, line_reference):
        if name in self.symbols:
            if line_reference not in self.symbols[name].line_reference and line_reference != self.symbols[name].line_declaration:
                self.symbols[name].add_reference(line_reference)
        else:
            name = re.sub(r'\b(int|float|char|bool)\b', ' ', name)
            if not name.isspace():
                self.error[name] = line_reference

    def parse_code(self, code):
        lines = code.split('\n')
        current_line = 1

        for line in lines:
            match = re.match(
                r'^\s*\b(int|float|char|bool)\b\s+([a-zA-Z_][a-zA-Z0-9_]*)(\s*\[\s*\d+\s*\])*(\s*\[\s*\d+\s*\])*\s*;',
                line)
            if match:
                declaration_sent = match.group()
                variable_type = match.group(1)
                variable_name = match.group(2)
                obj_address = hex(id(variable_name))
                dimension = 0
                if '[' in declaration_sent:
                    dimension = declaration_sent.count('[')
                self.add_variable(variable_name, obj_address, variable_type, dimension, current_line)

            references = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*=\s*;)',
                                    re.sub(r'\'[^\']*\'|\"[^\"]*\"', '', line))
            for reference in references:
                self.add_reference(reference.strip(), current_line)

            current_line += 1

    def display_table(self):
        print("Symbol Table:")
        print(
            "{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format('Counter', 'Variable Name', 'Obj Address', 'Type',
                                                                     'Dimension', 'Line Declaration', 'Line Reference'))
        for symbol in self.symbols.values():
            print("{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format(symbol.counter, symbol.name,
                                                                           symbol.obj_address, symbol.variable_type,
                                                                           symbol.dimension, symbol.line_declaration,
                                                                           ', '.join(map(str, symbol.line_reference))))

        for name, line in self.error.items():
            print(f'Error: Undeclared variable __{name}__ in line {line}', file=sys.stderr)

        for symbol in self.symbols.values():
            if len(symbol.line_reference) == 0:
                print(f'Warning: Unused variable __{symbol.name}__ declared in line {symbol.line_declaration}')
