class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def parse_program(tokens):
    root = TreeNode("program")
    root.add_child(parse_statement_list(tokens))
    return root


def parse_statement_list(tokens):
    node = TreeNode("statement_list")
    while tokens and tokens[0].value != ';':
        node.add_child(parse_statement(tokens))
        if tokens[0].value == ';':
            tokens.pop(0)  # consume the ';'
    return node


def parse_statement(tokens):
    if tokens[0].value in ['int', 'float', 'char']:
        return parse_declaration(tokens)
    else:
        return parse_assignment(tokens)


def parse_declaration(tokens):
    node = TreeNode("declaration")
    node.add_child(TreeNode(tokens.pop(0).value))  # type
    node.add_child(TreeNode(tokens.pop(0).value))  # identifier
    if tokens[0].value == '[':
        node.add_child(TreeNode(tokens.pop(0).value))  # '['
        node.add_child(TreeNode(tokens.pop(0).value))  # constant
        node.add_child(TreeNode(tokens.pop(0).value))  # ']'
        if tokens[0].value == '[':
            node.add_child(TreeNode(tokens.pop(0).value))  # '['
            node.add_child(TreeNode(tokens.pop(0).value))  # constant
            node.add_child(TreeNode(tokens.pop(0).value))  # ']'
    return node


def parse_assignment(tokens):
    node = TreeNode("assignment")
    node.add_child(TreeNode(tokens.pop(0).value))  # identifier
    node.add_child(TreeNode(tokens.pop(0).value))  # '='
    node.add_child(parse_expression(tokens))
    return node


def parse_expression(tokens):
    node = TreeNode("expression")
    node.add_child(TreeNode(tokens.pop(0).value))  # identifier or constant
    if tokens and tokens[0].value == '+':
        node.add_child(TreeNode(tokens.pop(0).value))  # '+'
        node.add_child(parse_expression(tokens))
    return node


def print_tree(node, indent=0, last_child=False):
    if indent > 0:
        prefix = "│   " * (indent - 1) + ("└── " if last_child else "├── ")
    else:
        prefix = ""
    print(prefix + node.value)
    for index, child in enumerate(node.children):
        print_tree(child, indent + 1, index == len(node.children) - 1)
