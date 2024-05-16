from collections import defaultdict


class UnorderedSymbolTable:
    def __init__(self):
        self.table = []

    def insert(self, variable, type="NUMBER"):
        self.table.append((variable, type))

    def lookup(self, variable):
        for entry in self.table:
            if entry[0] == variable:
                return entry[1]
        return None


class OrderedSymbolTable:
    def __init__(self):
        self.table = []

    def insert(self, variable, type="NUMBER"):
        self.table.append((variable, type))
        self.table.sort()
        # self.table.sort(key=lambda x: x[0])

    def lookup(self, variable):
        for entry in self.table:
            if entry[0] == variable:
                return entry[1]
        return None


class TreeNode:
    def __init__(self, variable, type):
        self.variable = variable
        self.type = type
        self.left = None
        self.right = None

class TreeSymbolTable:
    def __init__(self):
        self.root = None

    def insert(self, variable):
        self.root = self._insert_recursive(self.root, variable, "NUMBER")

    def _insert_recursive(self, node, variable, type):
        if node is None:
            return TreeNode(variable, type)
        if variable < node.variable:
            node.left = self._insert_recursive(node.left, variable, type)
        elif variable > node.variable:
            node.right = self._insert_recursive(node.right, variable, type)
        return node

    def lookup(self, variable):
        return self._lookup_recursive(self.root, variable)

    def _lookup_recursive(self, node, variable):
        if node is None:
            return None
        if variable == node.variable:
            return node.type
        elif variable < node.variable:
            return self._lookup_recursive(node.left, variable)
        else:
            return self._lookup_recursive(node.right, variable)

class HashTableSymboleTable:
    def __init__(self):
        self.variables = []
        self.table = defaultdict(list)

        # self.table = None
    
    def insert(self, variable):
        self.variables.append(variable)

    def lookup(self, variable):
        if variable in self.variables:
            return True
        return False
    
    def hash_variables(self):
        
        
        for variable in self.variables:
            hash = ( ord(variable[0]) + len(variable) ) % len(self.variables)

            self.table[hash].append((variable, "NUMBER"))

        return list(self.table.items())

    

