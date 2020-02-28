from tree import Node
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
        s = s.replace('('+ sub + ')', '(')
    ops, values = tokenize(s)

    for i, value in enumerate(values):
        if value.data == '(':
            values[i] = nodes[i]

    for op in operations:
        while op in ops:
            oi = ops.index(op)
            if op in '*+?':
                result = makeNode(values[oi], values[oi+1], op)
                del values[oi:oi+2]
            else:
                result = makeNode(values[oi], op)
                del values[oi]
            del ops[oi]
                
            values.insert(oi, result)
    return values[0]