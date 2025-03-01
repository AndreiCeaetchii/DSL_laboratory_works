from Laboratory2.finiteAutomation import FiniteAutomaton, Grammar

# Type 0
non_terminals = ['S', 'A']
terminals = ['a', 'b']
rules = {
    'Sab': ['ba'],
    'A': ['S']
}
grammar = Grammar(non_terminals, terminals, rules)
print(grammar.type.value)


# Type 1
non_terminals = ['S', 'A']
terminals = ['a', 'b', 'c']
rules = {
    'S': ['AB'],
    'A': ['abc'],
    'B': ['b']
}
grammar = Grammar(non_terminals, terminals, rules)
print(grammar.type.value)

# Type 2
non_terminals = ['S', 'A', 'B']
terminals = ['a', 'b', 'c']
rules = {
    'S': ['ABa'],
    'A': ['a'],
    'B': ['b']
}
grammar = Grammar(non_terminals, terminals, rules)
print(grammar.type.value)


# Type 3 (right linear)
non_terminals = ['S', 'B', 'C', 'D']
terminals = ['a', 'b', 'c']
rules = {
    'S': ['aB', 'aB'],
    'B': ['bS', 'aC', 'c'],
    'C': ['bD'],
    'D': ['c', 'aC']
}
grammar = Grammar(non_terminals, terminals, rules)
print(grammar.type.value)

# Type 3 (left linear)
non_terminals = ['S', 'B', 'C', 'D']
terminals = ['a', 'b', 'c']
rules = {
    'S': ['Ba', 'Baa'],
    'B': ['Sb', 'Ca', 'c'],
    'C': ['Db'],
    'D': ['c', 'Ca']
}
grammar = Grammar(non_terminals, terminals, rules)
print(grammar.type.value)

states = ['q0', 'q1', 'q2', 'q3', 'q4']
alphabet = ['a', 'b']
transitions = {
    'q0': {
        'a': ['q1'],  # δ(q0, a) = q1
        'b': []       # no transition on b from q0
    },
    'q1': {
        # no transition on a from q1 in the description
        'a': [],
        # δ(q1, b) = q1 and δ(q1, b) = q2 (two possibilities)
        'b': ['q1', 'q2']
    },
    'q2': {
        'a': ['q4'],  # δ(q2, a) = q4
        'b': ['q3']   # δ(q2, b) = q3
    },
    'q3': {
        'a': ['q1'],  # δ(q3, a) = q1
        'b': []       # no transition on b from q3
    },
    'q4': {
        # once we reach q4, no further transitions are specified
        'a': [],
        'b': []
    }
}
initial_state = 'q0'
accept_states = ['q4']

fa = FiniteAutomaton(states, alphabet, transitions, initial_state, accept_states)
fa.create_diagram().render('my_automaton', format='pdf', view=True)

print('FA to Regular Grammar conversion')
rg = fa.to_reg_gr()

print(rg.type.value)
print(f'Start: {rg.start}')
print(f'Non-terminals: {rg.non_terminals}')
print(f'Terminals: {rg.terminals}')
print('Rules:')
for nt, rules in rg.rules.items():
    print(f'{nt} -> {" | ".join(rules)}')

var = fa.is_dfa
print(f'FA is DFA: {var}')

print('NFA to DFA conversion')
nfa = fa
dfa = nfa.to_dfa()
print("Transitions:")
for state, transitions in dfa.transitions.items():
    print(f"Transitions from {state}:")
    for symbol, next_state in transitions.items():
        print(f"  {symbol} -> {next_state}")

dfa.create_diagram().render('my_automaton', format='pdf', view=True)