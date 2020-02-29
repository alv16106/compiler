from tree import Node
from utils import print2D
operations = '*+?.|'


def makeNode(op, *elements):
    if op == '*' or op == '+' or op == '?':
        return Node(left=elements[0], data=op)
    elif op == '.' or op == '|':
        return Node(left=elements[0], right=elements[1], data=op)
    raise EnvironmentError

def tokenize(s):
    ops = []
    symbols = []
    for c in s:
        if c == ' ':
            pass
        elif c in operations:
            ops.append(c)
        else:
            symbols.append(c)
    symbols = [Node(data=s) for s in symbols]
    return ops, symbols

def evaluate(s):
    nodes = []
    while '(' in s:
        sub = s[s.find('(')+1:s.rfind(')')]
        temp_value = evaluate(sub)
        nodes.append(temp_value)
        print(temp_value)
        s = s.replace('('+ sub + ')', ')')
    ops, values = tokenize(s)

    for i, value in enumerate(values):
        if value.data == ')':
            values[i] = nodes[i]
    print(len(ops), len(values))
    for op in operations:
        while op in ops:
            oi = ops.index(op)
            if op in '|.':
                result = makeNode(op, values[oi], values[oi+1])
                del values[oi:oi+2]
            else:
                result = makeNode(op, values[oi])
                del values[oi]
            del ops[oi]
                
            values.insert(oi, result)
    return values[0]

if __name__ == "__main__":
    inp = input('Regex: ')
    Tree = evaluate(inp)
    print2D(Tree)