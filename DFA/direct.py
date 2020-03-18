from NFA.constants import EPSILON, operations

def nullable(node):
    data = node.data
    if data == EPSILON:
        return True
    if data not in operations:
        return False
    
    if data in '*?':
        return True
    if data == '+':
        return nullable(node.left)
    if data == '|':
        return nullable(node.left) or nullable(node.right)
    if data == '.':
        return nullable(node.left) and nullable(node.right)

def firstPos(node):
    data = node.data
    fp = set()
    if data == EPSILON:
        return fp
    if data not in operations:
        fp.add(node.pos)
    
    if data in '*+?':
        fp = firstPos(node.left)
    if data == '|':
        fp = firstPos(node.left).union(firstPos(node.right))
    if data == '.':
        if nullable(node.left):
            fp = firstPos(node.left).union(firstPos(node.right))
        else:
            fp = firstPos(node.left)

    return fp

def lastPos(node):
    data = node.data
    lp = set()
    if data == EPSILON:
        return lp
    if data not in operations:
        lp.add(node.pos)
    
    if data in '*+?':
        lp = lastPos(node.left)
    if data == '|':
        lp = lastPos(node.left).union(lastPos(node.right))
    if data == '.':
        if nullable(node.right):
            lp = lastPos(node.left).union(lastPos(node.right))
        else:
            lp = lastPos(node.right)

    return lp

def followPos(root, fpos={}, symbols={}):
    if not root:
        return

    if root.data not in operations:
        symbols[root.data].add(root.pos)
    
    followPos(root.right, fpos, symbols)
    followPos(root.left, fpos, symbols)

    if root.data == '.':
        for p in lastPos(root.left):
            fpos[p].update(firstPos(root.right))
    if root.data in '*+':
        for p in lastPos(root):
            fpos[p].update(firstPos(root))
    return fpos, symbols

def build(root, vocab):
    symbolpos = {}
    for symbol in vocab:
        symbolpos[symbol] = set()
    fpos, symbolpos = followPos(root, {}, symbolpos)
    current = 0
    Dstates = []
    s0 = firstPos(root)
    isAccepting = symbolpos['#'] in s0
    Dstates.append(s0)
    visited = {}
    visited[current] = State(name=current, accepting=isAccepting)
    for index, T in enumerate(Dstates):
        for symbol in vocab:
            new = set()
            s = T.intersection(symbolpos[symbol])
            for a in s:
                new.update(fpos[a])
            if new not in Dstates:
                current += 1
                isAccepting = symbolpos['#'] in new
                print('state', current, isAccepting)
                visited[current] = State(name=current, accepting=isAccepting)
                Dstates.append(new)
                visited[index].addTransition(symbol, visited[current])
            else:
                transition = Dstates.index(new)
                visited[index].addTransition(symbol, visited[transition])
    return visited