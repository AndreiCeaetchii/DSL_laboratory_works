import random

from Laboratory1.finiteAutomation import FiniteAutomaton


class Grammar:
    def __init__(self, non_terminals, terminals, rules, start='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start = start
        self.type = self.get_type()

    def generate_string(self, symbol=None, len=0, max_len=15):
        # If no symbol is provided, use the start symbol
        if symbol is None:
            symbol = self.start

        # Check for exceeding the maximum length
        if len > max_len:
            return ''

        # Base case: symbol is terminal
        if symbol in self.terminals:
            return symbol

        if symbol in self.rules:
            # Random production
            production = random.choice(self.rules[symbol])
            result = ''
            for sym in production:
                result += self.generate_string(sym, len + 1, max_len)
            return result

        # The symbol doesn't match anything in the production
        return ''

    def get_type(self):
        left, right = False, False

        # Flatten the list of production rules to easily iterate over each right side
        rhs = [item for inner_list in self.rules.values() for item in inner_list]
        # Iterate over each right side of the production rules that have 2 symbols
        for right_side in filter(lambda x: len(x) == 2, rhs):
            # If the first symbol is a terminal and the second is a non-terminal, it's a right regular rule
            if right_side[0] in self.terminals and right_side[1] in self.non_terminals:
                right = True
            # If the first symbol is a non-terminal and the second is a terminal, it's a left regular rule
            elif right_side[0] in self.non_terminals and right_side[1] in self.terminals:
                left = True
            # If neither of the above conditions is met, the production rule format is invalid
            else:
                raise ValueError('Invalid production rule format')

        # If both left and right are True, the grammar is not regular
        if left and right:
            raise ValueError('The grammar is not regular')

        if left:
            return 'left'

        return 'right'

    def convert_to_fa(grammar):
        final_state = 'DEAD'
        transitions = {}

        for non_terminal in grammar.non_terminals:
            transitions[non_terminal] = {}

        for non_terminal, productions in grammar.rules.items():
            for production in productions:
                if len(production) == 1:  # Single terminal production
                    transitions[non_terminal][production] = final_state
                elif grammar.type == 'right':  # Right-linear production
                    transition, new_state = production[0], production[1]
                    transitions[non_terminal][transition] = new_state
                elif grammar.type == 'left':  # Left-linear production
                    transition, new_state = production[1], production[0]
                    transitions[non_terminal][transition] = new_state

        return FiniteAutomaton(
            states=grammar.non_terminals + [final_state],
            alphabet=grammar.terminals,
            transitions=transitions,
            initial_state=grammar.start,
            accept_states=[final_state]
        )