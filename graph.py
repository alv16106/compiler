# Para graficar 
from graphviz import Digraph


def graph(automata):
    dot = Digraph(name = "Automata")
    dot.attr(rankdir = "LR")
    for state in automata.states:
        if state.accept:
            dot.node(str(state.id), str(state.id), shape = "doublecircle")
        else:
            dot.node(str(state.id), str(state.id))
        for transition in state.transitions:
            dot.edge(str(state.id),str(transition.to), transition.symbol)
    print(dot.source)
    dot.render('test-output/automata.gv', view=False)
