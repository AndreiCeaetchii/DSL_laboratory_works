from __future__ import annotations

from graphviz import Digraph
from ast_definitions import ASTNode

_CHILD_ATTRS = (
    "target_flag",
    "command_sequence",
    "flags",
    "next_command",
)

def render_ast_diagram(node: ASTNode, graph: Digraph | None = None,
                       parent: str | None = None) -> Digraph:
    """
    Recursively walk *node* and build a Graphviz diagram.

    Parameters
    ----------
    node   : current AST node or primitive value
    graph  : the Digraph being built (created on first call)
    parent : id of the parent node in Graphviz (for edges)

    Returns
    -------
    graph  : the completed Digraph (handy for chaining)
    """
    if graph is None:
        graph = Digraph(
            node_attr={
                "shape": "box",
                "style": "rounded,filled",
                "fontname": "Helvetica",
                "fillcolor": "#eef",
            }
        )

    if isinstance(node, ASTNode):
        label_lines = [node.__class__.__name__, node.name]
        if getattr(node, "value", None) is not None:
            label_lines.append(f"value = {node.value}")
        label = "\n".join(label_lines)

        node_id = str(id(node))

        graph.node(node_id, label)

        if parent is not None:
            graph.edge(parent, node_id)

        for attr in _CHILD_ATTRS:
            child = getattr(node, attr, None)
            if not child:
                continue

            if isinstance(child, list):
                for c in child:
                    render_ast_diagram(c, graph, node_id)
            else:
                render_ast_diagram(child, graph, node_id)

    elif isinstance(node, (str, int)):  # primitive leaf
        node_id = str(id(node))
        graph.node(node_id, str(node))
        if parent is not None:
            graph.edge(parent, node_id)

    return graph
