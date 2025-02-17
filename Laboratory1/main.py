from Laboratory1.grammar import Grammar

non_terminals= ['S', 'I', 'J', 'K']
terminals = ['a', 'b', 'c', 'e', 'n', 'f', 'm']
rules = {
    'S': ['cI'],
    'I': ['bJ', 'fI', 'e', 'eK'],
    'J': ['nJ', 'cS'],
    'K': ['nK', 'm']
}


grammar = Grammar(non_terminals, terminals, rules)
dfa = grammar.convert_to_fa()

print(f"Alphabet: {dfa.alphabet}")
print(f"States: {dfa.states}")
print(f"Initial state: {dfa.initial_state}")
print(f"Accepted states: {dfa.accept_states}")
print("Transitions:")
for state, transitions in dfa.transitions.items():
    print(f"Transitions from {state}:")
    for symbol, next_state in transitions.items():
        print(f"  {symbol} -> {next_state}")

print("Generated strings:")
for _ in range(5):
    gen_string = grammar.generate_string(max_len=15)
    print(f"{gen_string} ({'accepted' if dfa.accepts(gen_string) else 'rejected'})")

tested_strings = ['cnnccfeeee', 'cfnnccfbccbncce', 'cnnccncce', 'cnnccncceee']
for string in tested_strings:
    print(f"{string} - {'accepted' if dfa.accepts(string) else 'rejected'}")