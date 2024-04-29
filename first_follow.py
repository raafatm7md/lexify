from tabulate import tabulate


def compute_first(grammar):
    first_sets = {}
    for non_terminal in list(grammar.keys()):
        first_set = set()
        for production in grammar.get(non_terminal):
            res = find_first_symbols(production, grammar)
            if res is not None:
                if type(res) is list:
                    for element in res:
                        first_set.add(element)
                else:
                    first_set.add(res)
        first_sets[non_terminal] = first_set
    return first_sets


def find_first_symbols(symbol_sequence, grammar):
    if len(symbol_sequence) != 0 and (symbol_sequence is not None):
        if symbol_sequence[0] in terminal_symbols:
            return symbol_sequence[0]
        elif symbol_sequence[0] == 'ε':
            return 'ε'
    if len(symbol_sequence) != 0:
        if symbol_sequence[0] in list(grammar.keys()):
            first_result = []
            rhs_productions = grammar[symbol_sequence[0]]
            for rhs in rhs_productions:
                individual_result = find_first_symbols(rhs, grammar)
                if type(individual_result) is list:
                    for element in individual_result:
                        first_result.append(element)
                else:
                    first_result.append(individual_result)
            if 'ε' not in first_result:
                return first_result
            else:
                first_result.remove('ε')
                if len(symbol_sequence) > 1:
                    new_result = find_first_symbols(symbol_sequence[1:], grammar)
                    if new_result is not None:
                        if type(new_result) is list:
                            updated_list = first_result + new_result
                        else:
                            updated_list = first_result + [new_result]
                    else:
                        updated_list = first_result
                    return updated_list
                first_result.append('ε')
                return first_result


def compute_follow(grammar):
    follow_sets = {}
    for non_terminal in grammar:
        follow_set = set()
        sol = find_follow_symbols(non_terminal, grammar)
        if sol is not None:
            for element in sol:
                follow_set.add(element)
        follow_sets[non_terminal] = follow_set
    return follow_sets


def find_follow_symbols(non_terminal, grammar):
    follow_set = set()
    if non_terminal == list(grammar.keys())[0]:
        follow_set.add('$')
    for current_non_terminal in grammar:
        rhs_productions = grammar[current_non_terminal]
        for production in rhs_productions:
            if non_terminal in production:
                while non_terminal in production:
                    index_nt = production.index(non_terminal)
                    production = production[index_nt + 1:]
                    if len(production) != 0:
                        res = find_first_symbols(production, grammar)
                        if 'ε' in res:
                            res.remove('ε')
                            new_result = find_follow_symbols(current_non_terminal, grammar)
                            if new_result is not None:
                                if type(new_result) is list:
                                    updated_list = res + new_result
                                else:
                                    updated_list = res + [new_result]
                            else:
                                updated_list = res
                            res = updated_list
                    else:
                        if non_terminal != current_non_terminal:
                            res = find_follow_symbols(current_non_terminal, grammar)
                    if res is not None:
                        if type(res) is list:
                            for element in res:
                                follow_set.add(element)
                        else:
                            follow_set.add(res)
    return list(follow_set)


def generate_parse_table(grammar, non_terminals, terminal_symbols, follow_sets):
    parse_table = {}
    terminal_symbols.append('$')
    for non_terminal in non_terminals:
        parse_table[non_terminal] = {}
        for terminal in terminal_symbols:
            parse_table[non_terminal][terminal] = None

    for non_terminal in grammar:
        productions = grammar[non_terminal]
        for production in productions:
            first_of_production = find_first_symbols(production, grammar)
            if type(first_of_production) is list:
                for symbol in first_of_production:
                    if symbol != 'ε':
                        parse_table[non_terminal][symbol] = production
            else:
                if first_of_production != 'ε':
                    parse_table[non_terminal][first_of_production] = production

            if 'ε' in first_of_production:
                for follow_symbol in follow_sets[non_terminal]:
                    parse_table[non_terminal][follow_symbol] = production

    return parse_table


def print_parse_table(parse_table):
    headers = list(parse_table[non_terminals[0]].keys())
    rows = []
    for non_terminal in parse_table:
        row = [non_terminal]
        for terminal in parse_table[non_terminal]:
            row.append(parse_table[non_terminal][terminal])
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt='grid'))


def read_grammar(file_name):
    grammar = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.replace('#', 'ε')
            line = line.replace('1', '\'')
            if line:
                non_terminal, productions = line.split('->')
                non_terminal = non_terminal.strip()
                productions = [p.strip().split() for p in productions.split('|')]
                grammar[non_terminal] = productions
    non_terminals = list(grammar.keys())
    terminal_symbols = set()
    for value in grammar.values():
        for symbols in value:
            for symbol in symbols:
                if symbol not in non_terminals:
                    terminal_symbols.add(symbol)
    terminal_symbols = list(terminal_symbols)
    return grammar, non_terminals, terminal_symbols


grammar_file = 'grammar.txt'
grammar, non_terminals, terminal_symbols = read_grammar(grammar_file)

first_sets = compute_first(grammar)
print('First: ')
for non_terminal in first_sets:
    print(f'first({non_terminal}) -> {first_sets[non_terminal]}')

follow_sets = compute_follow(grammar)
print('\nFollow: ')
for non_terminal in follow_sets:
    print(f'follow({non_terminal}) -> {follow_sets[non_terminal]}')

parse_table = generate_parse_table(grammar, non_terminals, terminal_symbols, follow_sets)

print("\nParse Table:")
print_parse_table(parse_table)
