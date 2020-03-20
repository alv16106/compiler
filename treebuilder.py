from tree import Node
from utils import print2D
import DFA.direct as dfa
operations = '*+?.|'


def makeNode(op, *elements):
    if op == '*' or op == '+' or op == '?':
        return Node(left=elements[0], data=op)
    elif op == '.' or op == '|':
        return Node(left=elements[0], right=elements[1], data=op)
    raise EnvironmentError

def tokenize(s, pos):
    ops = []
    symbols = []
    for c in s:
        if c == ' ':
            pass
        elif c in operations:
            ops.append(c)
        else:
            symbols.append(c)
    for i, s in enumerate(symbols):
        if s not in '~ε':
            pos += 1
        symbols[i] = Node(data=s, pos=pos)
    return ops, symbols, pos

def evaluate(s, pos):
    nodes = []
    while '(' in s:
        print('Entra', s)
        sub = s[s.find('(')+1:s.find(')')]
        while sub.count('(') != sub.count(')'):
            dif = abs(sub.count('(') - sub.count(')'))
            if sub.count('(') < sub.count(')'):
                closing = s.replace(')', 'X', dif).find(')')
                sub = s[s.find('(')+1:s.find(')',closing+1)]
            else:
                closing = s.replace(')', 'X', dif).find(')') 
                sub = s[s.find('(') + 1:s.find(')', closing)]
        temp_value, pos = evaluate(sub, pos)
        nodes.append(temp_value)
        print(temp_value)
        s = s.replace('('+ sub + ')', '~', 1)
        print('After ', s)
    ops, values, pos = tokenize(s, pos)

    c = 0
    for i, value in enumerate(values):
        if value.data == '~':
            values[i] = nodes[c]
            c += 1
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
    return values[0], pos

if __name__ == "__main__":
    inp = input('Regex: ')
    Tree, positions = evaluate(inp, 0)
    follow = {}
    pos = {}
    vocab = set(inp) - set(operations) - set('()')
    for p in range(positions):
        follow[p+1] = set()
    for a in vocab:
        pos[a] = set()
    followpos, s = dfa.followPos(Tree, follow, pos)
    print(followpos)
    print(s)
    print2D(Tree)