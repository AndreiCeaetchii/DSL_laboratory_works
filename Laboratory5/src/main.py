from Grammar import Grammar
from constants import *

import unittest
from test_grammar import TestGrammar

non_terminals = ['S', 'A', 'B', 'C', 'E']
terminals = ['a', 'b']
rules = {
    'S': ['aB', 'AC'],
    'A': ['a', 'ASC', 'BC'],
    'B': ['b', 'bS'],
    'C': ['BA', EPSILON],
    'E': ['bB']
}

grammar = Grammar(non_terminals, terminals, rules)

print('Original grammar:')
grammar.print_rules()

print('\nConverting to CNF:')
grammar.to_cnf()

unittest.main(argv=[''], exit=False)
