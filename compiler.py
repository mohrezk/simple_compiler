import re
from symbol_table import *

TOKEN_TYPES = [
    ("NUMBER", r"\d+"),
    ("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    ("ASSIGN", r"="),
    ("WHITESPACE", r"\s+"),
]


def tokenize(src) -> list:
    tokens = []
    while src:
        for token_type, pattern in TOKEN_TYPES:
            match = re.match(pattern, src)            
            if match:
                token_value = match.group(0)
                if token_type != "WHITESPACE":
                    tokens.append((token_type, token_value))
                src = src[match.end() :]
                break
        else:
            raise Exception("Invalid character: " + src[0])
    return tokens



# Stmt       -> Assignment 
# Assignment -> VARIABLE = Expr
# Expr   -> Term ((PLUS | MINUS) Term)*
# Term   -> Factor ((MULTIPLY | DIVIDE) Factor)*
# Factor -> NUMBER | VARIABLE | LPAREN Expr RPAREN


class Parser:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()
        self.symbol_table = symbol_table

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def check(self, expected_token):
        if self.current_token:
            if self.current_token[0] == expected_token:
                token = self.current_token
                self.advance()
                return token
            else:
                raise SyntaxError(f"Expected {expected_token}")
        else:
            raise SyntaxError(f"Expected {expected_token}")

    def factor(self):
        token = self.current_token
        if token:
            if token[0] == "NUMBER":
                self.advance()
                return ("NUMBER", token[1])
            
            elif token[0] == "VARIABLE":
                if self.tokens[self.token_index - 1][0] in ("ASSIGN", "MULTIPLY", "PLUS", "MINUS", "DIVIDE", "LPAREN", "RPAREN"):
                    if not self.symbol_table.lookup(token[1]):
                        raise SyntaxError(f"{token[1]} is not defined")
                self.advance()
                return ("VARIABLE", token[1])
            
            elif token[0] == "LPAREN":
                self.advance()
                expression_result = self.expression()
                if self.current_token[0] == "RPAREN":
                    self.advance()
                    return expression_result
                else:
                    raise SyntaxError("Expected closing parenthesis")
        else:
            raise SyntaxError("Invalid syntax")

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token[0] in ("MULTIPLY", "DIVIDE"):
            token = self.current_token
            self.advance()
            right = self.factor()
            result = (token[0], result, right)
        return result

    def expression(self):
        result = self.term()
        while self.current_token and self.current_token[0] in ("PLUS", "MINUS"):
            token = self.current_token
            self.advance()
            right = self.term()
            result = (token[0], result, right)

        return result

    def assignment(self):
        variable_name = self.current_token[1]
        self.advance()  

        if not self.current_token or self.current_token[0] != "ASSIGN":
            raise SyntaxError("Expected '=' for assignment")
        
        self.advance() 

        value = self.expression()

        if not self.symbol_table.lookup(variable_name):
            self.symbol_table.insert(variable_name)


        return ("ASSIGN", variable_name, value)

    
    def parse(self):
        parse_trees = []
        while self.token_index < len(self.tokens):
            if self.current_token[0] == "VARIABLE":
                tree = self.assignment()
                parse_trees.append(tree)

            else:
                raise SyntaxError("Syntax error")


        return parse_trees


def build_with_unordered_table(tokens):
    unordered_symbol_table = UnorderedSymbolTable()
    parser = Parser(tokens, unordered_symbol_table) 
    parse_tree = parser.parse()
    return parse_tree, unordered_symbol_table.table

def build_with_ordered_table(tokens):
    ordered_symbol_table = OrderedSymbolTable()
    parser = Parser(tokens, ordered_symbol_table) 
    parse_tree = parser.parse()
    return parse_tree, ordered_symbol_table.table

def build_with_tree_table(tokens):
    tree_symbol_table = TreeSymbolTable() 
    parser = Parser(tokens, tree_symbol_table) 
    parse_tree = parser.parse()

    root = tree_symbol_table.root

    table = []

    def dfs(root):
        if not root:
            return
        table.append((root.variable, root.type))
        dfs(root.left)
        dfs(root.right)
    
    dfs(root)
    return parse_tree, table

def build_with_hash_table(tokens):
    hash_symbol_table  = HashTableSymboleTable()
    parser = Parser(tokens, hash_symbol_table) 
    parse_tree = parser.parse()

    return parse_tree, hash_symbol_table.hash_variables()

def main():
    src = open("zfile.txt", "r").read()

    tokens = tokenize(src)
    print(len(tokens))
    parse_tree, table = build_with_unordered_table(tokens)

    print("TOKENS")
    for token in tokens:
        print(token)
    print("=" * 80)

    print("PARSE TREE")
    for tree in parse_tree:
        print(tree)
    print("=" * 80)

    print("Table", table)


if __name__ == "__main__":
    main()




