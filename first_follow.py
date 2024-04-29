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
    terminals = set()
    for value in grammar.values():
        for symbols in value:
            for symbol in symbols:
                if symbol not in non_terminals:
                    terminals.add(symbol)
    terminals = list(terminals)
    return grammar, non_terminals, terminals


grammar = 'grammar.txt'
grammar, non_terminals, terminals = read_grammar(grammar)

