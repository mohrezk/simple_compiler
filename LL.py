import pprint

class LLParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {non_terminal: set() for non_terminal in self.grammar}
        self.follow = {non_terminal: set() for non_terminal in self.grammar}
        self.table = {}

    def calculate_first(self):
        for non_terminal in self.grammar:
            self.first[non_terminal] = self.calculate_first_for(non_terminal)

    def calculate_first_for(self, symbol):
        result = set()
        if not symbol.isupper():  # Single terminal symbol
            return {symbol}
        if len(symbol) > 1:  # More than one symbol, split it
            first_of_first_symbol = self.calculate_first_for(symbol[0])  
            if '' in first_of_first_symbol:
                return first_of_first_symbol - {''} | self.calculate_first_for(symbol[1:])
            return first_of_first_symbol
        for production in self.grammar[symbol]:  # Single non-terminal symbol
            if production == '':
                result.add('')
            else:
                for sym in production:
                    first_of_sym = self.calculate_first_for(sym)
                    result.update(first_of_sym - {''})
                    if '' not in first_of_sym:
                        break
                else:
                    result.add('')
        return result

    def calculate_follow(self):
        self.follow[next(iter(self.grammar))].add('$')  # Add $ to the start symbol
        for non_terminal in self.grammar:
            for production in self.grammar[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol.isupper():
                        next_symbol_first = self.calculate_first_for(production[i+1:]) if i+1 < len(production) else {'$'}
                        self.follow[symbol].update(next_symbol_first - {''})
                        if '' in next_symbol_first:
                            self.follow[symbol].update(self.follow[non_terminal])

    def build_table(self):
        for non_terminal in self.grammar:
            self.table[non_terminal] = {}
            for production in self.grammar[non_terminal]:
                first_of_production = self.calculate_first_for(production)
                for terminal in first_of_production - {''}:
                    self.table[non_terminal][terminal] = production
                if '' in first_of_production:
                    for follow_symbol in self.follow[non_terminal]:
                        self.table[non_terminal][follow_symbol] = production

    def parse(self, tokens):
        tokens = tokens + ['$']
        stack = ['$']
        stack.append(next(iter(self.grammar)))  # Start symbol
        current_token_index = 0

        while stack:
            top = stack.pop()
            current_token = tokens[current_token_index]
            if top == current_token:
                current_token_index += 1
            elif top.isupper() and current_token in self.table[top]:
                stack.extend(reversed(self.table[top][current_token]))
            else:
                return False
        return True

    def print_table(self):
        print("LL(1) Parsing Table:")
        pprint.pprint(self.table, width=1)




grammar = {
    'E': ['TA'],
    'A': ['+TA', ''],
    'T': ['FB'],
    'B': ['*FB', ''],
    'F': ['(E)', 'v']
}


# Example usage:
# grammar = {
#     'S': ['bXY'],
#     'X': ['b', 'c'],
#     'Y': ['b', '']
# }

parser = LLParser(grammar)
parser.calculate_first()
parser.calculate_follow()
parser.build_table()


for non_terminal, first_set in parser.first.items():
    print(non_terminal, first_set)

print("\nFollow sets:")
for non_terminal, follow_set in parser.follow.items():
    print(non_terminal, follow_set)

print(parser.print_table())

print(parser.parse(['a', 'b']))  # Should return True
print(parser.parse(['b']))       # Should return True
print(parser.parse(['a']))       # Should return False