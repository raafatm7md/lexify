from tabulate import tabulate


def compute_first(grammar):
    first_sets = {nt: set() for nt in grammar}
    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            res = find_first_symbols(production, grammar)
            if res:
                first_sets[non_terminal].update(res)
    return first_sets


def find_first_symbols(symbol_sequence, grammar):
    if not symbol_sequence:
        return set()

    first_symbol = symbol_sequence[0]
    if first_symbol in terminal_symbols:
        return {first_symbol}
    if first_symbol == 'ε':
        return {'ε'}
    if first_symbol in grammar:
        result = set()
        for rhs in grammar[first_symbol]:
            individual_result = find_first_symbols(rhs, grammar)
            result.update(individual_result)
        if 'ε' in result and len(symbol_sequence) > 1:
            result.remove('ε')
            result.update(find_first_symbols(symbol_sequence[1:], grammar))
        return result
    return set()


def compute_follow(grammar):
    follow_sets = {nt: set() for nt in grammar}
    start_symbol = next(iter(grammar))
    follow_sets[start_symbol].add('$')

    for non_terminal in grammar:
        for rhs in grammar[non_terminal]:
            for i, symbol in enumerate(rhs):
                if symbol in grammar:
                    follow_set = follow_sets[symbol]
                    if i + 1 < len(rhs):
                        next_first = find_first_symbols(rhs[i + 1:], grammar)
                        follow_set.update(next_first - {'ε'})
                        if 'ε' in next_first:
                            follow_set.update(follow_sets[non_terminal])
                    else:
                        follow_set.update(follow_sets[non_terminal])
    return follow_sets


def generate_parse_table(grammar, non_terminals, terminal_symbols, follow_sets):
    parse_table = {nt: {t: None for t in terminal_symbols + ['$']} for nt in non_terminals}
    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            first_of_production = find_first_symbols(production, grammar)
            for symbol in first_of_production:
                if symbol != 'ε':
                    parse_table[non_terminal][symbol] = production
            if 'ε' in first_of_production:
                for follow_symbol in follow_sets[non_terminal]:
                    parse_table[non_terminal][follow_symbol] = production
    return parse_table


def print_parse_table(parse_table):
    headers = [''] + list(parse_table[next(iter(parse_table))].keys())
    rows = [
        [non_terminal] + [parse_table[non_terminal][t] for t in headers[1:]]
        for non_terminal in parse_table
    ]
    print(tabulate(rows, headers=headers, tablefmt='fancy_grid'))


def read_grammar(file_name):
    grammar = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip().replace('#', 'ε').replace('1', '\'')
            if line:
                non_terminal, productions = line.split('->')
                grammar[non_terminal.strip()] = [p.strip().split() for p in productions.split('|')]

    non_terminals = list(grammar.keys())
    terminal_symbols = {symbol for productions in grammar.values() for symbols in productions for symbol in
                        symbols} - set(non_terminals)
    return grammar, non_terminals, list(terminal_symbols)


grammar_file = 'grammar.txt'
grammar, non_terminals, terminal_symbols = read_grammar(grammar_file)

first_sets = compute_first(grammar)
print('First:')
for nt, first in first_sets.items():
    print(f'first({nt}) -> {first}')

follow_sets = compute_follow(grammar)
print('\nFollow:')
for nt, follow in follow_sets.items():
    print(f'follow({nt}) -> {follow}')

parse_table = generate_parse_table(grammar, non_terminals, terminal_symbols, follow_sets)

print("\nParse Table:")
print_parse_table(parse_table)
