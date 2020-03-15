from graphviz import Digraph

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

def graph(table):
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
    dot.render('test-output/automata.gv', view=False)