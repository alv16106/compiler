from graphviz import Digraph
import json

COUNT = [10]

def print2DUtil(root, space) : 
  
    # Base case  
    if (root == None) : 
        return
  
    # Increase distance between levels  
    space += COUNT[0] 
  
    # Process right child first  
    print2DUtil(root.right, space)  
  
    # Print current node after space  
    # count  
    print()
    for _ in range(COUNT[0], space): 
        print(end = " ")
    print(root.data)  
  
    # Process left child  
    print2DUtil(root.left, space)  
  
# Wrapper over print2DUtil()  
def print2D(root) : 
      
    # space=[0] 
    # Pass initial space count as 0  
    print2DUtil(root, 0)  

def graph(table, name='output'):
    dot = Digraph(name = "Automata")
    dot.attr(rankdir = "LR")
    for node in table:
        state = table[node]
        if state.accepting:
            dot.node(str(state.name), str(state.name), shape = "doublecircle")
        else:
            dot.node(str(state.name), str(state.name))
        for symbol, transitions in state.transitions.items():
            for t in transitions:
                dot.edge(str(state.name), str(t.name), symbol)
    print(dot.source)
    dot.render('test-output/' + name + '.gv', view=False)


def graphNFA(table, accepting, name='output'):
    dot = Digraph(name = name)
    dot.attr(rankdir = "LR")
    for state, transitions in table.items():
        if state in accepting:
            dot.node(str(state), str(state), shape = "doublecircle")
        else:
            dot.node(str(state), str(state))
        for symbol, to in transitions.items():
            for next_state in to:
                dot.edge(str(state), str(next_state), symbol)
    dot.render('test-output/' + name + '.gv', view=False)


def dfaToText(dfa, vocab, name):
    output = {'ESTADOS':[], 'ACEPTACION':[], 'TRANSICIONES':[]}
    output['SIMBOLOS'] = list(vocab)
    for key, state in dfa.items():
        output['ESTADOS'].append(key)
        if state.accepting:
            output['ACEPTACION'].append(key)
        for s, t in state.transitions.items():
            if t:
                temp_trans = [key, s, t.pop().name]
                output['TRANSICIONES'].append(temp_trans)
    print(output)
    with open('./textFiles/' + name + '.txt', 'w') as outfile:
        json.dump(output, outfile, indent=2)



def nfaToText(table, accept, vocab, name):
    output = {'ESTADOS':[], 'TRANSICIONES':[]}
    output['ACEPTACION'] = list(accept)
    output['SIMBOLOS'] = list(vocab)
    for state, transitions in table.items():
        output['ESTADOS'].append(state)
        for symbol, to in transitions.items():
            temp_trans = [[state, symbol, next_state] for next_state in to]
            output['TRANSICIONES'].extend(temp_trans)

    with open('./textFiles/' + name + '.txt', 'w') as outfile:
        json.dump(output, outfile, indent=2)