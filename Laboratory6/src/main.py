from lexer import lexer
from parser1 import parser1
from utils import render_ast_diagram


def generate_ast(input):
    result = parser1.parse(input)

    graph = render_ast_diagram(result)
    graph.render('ast', format='png', cleanup=True)


source = 'imp --target="./path/to/folder/" compress'

generate_ast(source)
