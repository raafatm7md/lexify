class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def parse_program(tokens):
    root = TreeNode("Program")
    root.add_child(parse_statement_list(tokens))
    if tokens:
        raise SyntaxError("Unexpected tokens at the end of the program")
    return root


def parse_statement_list(tokens):
    node = TreeNode("StatementList")
    while tokens and tokens[0].value != ';':
        node.add_child(parse_statement(tokens))
        if tokens[0].value == ';':
            tokens.pop(0)
    return node


def parse_statement(tokens):
    if tokens[0].value in ['int', 'float', 'char', 'bool']:
        return parse_declaration(tokens)
    elif tokens[0].value == 'if':
        return parse_if_statement(tokens)
    elif tokens[0].value == 'while':
        return parse_while_statement(tokens)
    elif tokens[0].value == 'print':
        return parse_print_statement(tokens)
    else:
        return parse_assignment(tokens)


def parse_declaration(tokens):
    node = TreeNode("Declaration")
    node.add_child(parse_type(tokens))
    node.add_child(TreeNode(tokens.pop(0).value))
    if tokens[0].value == '[':
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(TreeNode(tokens.pop(0).value))
        if tokens[0].value == '[':
            node.add_child(TreeNode(tokens.pop(0).value))
            node.add_child(TreeNode(tokens.pop(0).value))
            node.add_child(TreeNode(tokens.pop(0).value))
    if tokens and tokens[0].value == '=':
        tokens.pop(0)
        node.add_child(parse_expression(tokens))
    elif tokens and tokens[0].value != ';':
        raise SyntaxError("Expecting ';' or '=' after declaration")
    return node


def parse_assignment(tokens):
    node = TreeNode("Assignment")
    node.add_child(TreeNode(tokens.pop(0).value))
    if tokens[0].value == '[':
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(TreeNode(tokens.pop(0).value))
        if tokens[0].value == '[':
            node.add_child(TreeNode(tokens.pop(0).value))
            node.add_child(TreeNode(tokens.pop(0).value))
            node.add_child(TreeNode(tokens.pop(0).value))
    tokens.pop(0)
    node.add_child(parse_expression(tokens))
    if tokens and tokens[0].value != ';':
        raise SyntaxError("Expecting ';' after assignment")
    return node


def parse_if_statement(tokens):
    node = TreeNode("IfStatement")
    tokens.pop(0)
    tokens.pop(0)
    node.add_child(parse_condition(tokens))
    tokens.pop(0)
    tokens.pop(0)
    node.add_child(parse_statement_list(tokens))
    tokens.pop(0)
    if tokens and tokens[0].value == 'else':
        tokens.pop(0)
        tokens.pop(0)
        node.add_child(parse_statement_list(tokens))
        tokens.pop(0)
    return node


def parse_while_statement(tokens):
    node = TreeNode("WhileStatement")
    tokens.pop(0)
    tokens.pop(0)
    node.add_child(parse_condition(tokens))
    tokens.pop(0)
    tokens.pop(0)
    node.add_child(parse_statement_list(tokens))
    tokens.pop(0)
    return node


def parse_print_statement(tokens):
    node = TreeNode("PrintStatement")
    tokens.pop(0)
    tokens.pop(0)
    node.add_child(parse_expression(tokens))
    tokens.pop(0)
    tokens.pop(0)
    if tokens and tokens[0].value != ';':
        raise SyntaxError("Expecting ';' after print statement")
    return node


def parse_expression(tokens):
    node = TreeNode("Expression")
    node.add_child(parse_term(tokens))
    while tokens and tokens[0].value in ['+', '-']:
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(parse_term(tokens))
    return node


def parse_term(tokens):
    node = TreeNode("Term")
    node.add_child(parse_factor(tokens))
    while tokens and tokens[0].value in ['*', '/']:
        node.add_child(TreeNode(tokens.pop(0).value))
        node.add_child(parse_factor(tokens))
    return node


def parse_factor(tokens):
    node = TreeNode("Factor")
    if tokens[0].value.isdigit():
        node.add_child(TreeNode(tokens.pop(0).value))
    elif tokens[0].value.isalpha():
        node.add_child(TreeNode(tokens.pop(0).value))
    elif tokens[0].value[0] == '"':
        node.add_child(TreeNode(tokens.pop(0).value))
    else:
        tokens.pop(0)
        node.add_child(parse_expression(tokens))
        if tokens[0].value != ')':
            raise SyntaxError("Expecting ')' after expression")
        tokens.pop(0)
    return node


def parse_condition(tokens):
    node = TreeNode("Condition")
    node.add_child(parse_expression(tokens))
    node.add_child(TreeNode(tokens.pop(0).value))
    node.add_child(parse_expression(tokens))
    return node


def parse_type(tokens):
    return TreeNode(tokens.pop(0).value)


def print_tree(node, indent=0, last_child=False):
    if indent > 0:
        prefix = "│   " * (indent - 1) + ("└── " if last_child else "├── ")
    else:
        prefix = ""
    print(prefix + node.value)
    for index, child in enumerate(node.children):
        print_tree(child, indent + 1, index == len(node.children) - 1)
