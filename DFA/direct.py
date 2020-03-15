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
        return nullable(node.Left)
    if data == '|':
        return nullable(node.Left) or nullable(node.Right)
    if data == '.':
        return nullable(node.Left) and nullable(node.Right)

def firstPos(node):
    data = node.data
    fp = set()
    if data == EPSILON:
        return fp
    if data not in operations:
        fp.add(node.pos)
    
    if data in '*+?':
        fp = firstPos(node.Left)
    if data == '|':
        fp = firstPos(node.Left).union(firstPos(node.Right))
    if data == '.':
        if nullable(node.Left):
            fp = firstPos(node.Left).union(firstPos(node.Right))
        else:
            fp = firstPos(node.Left)

    return fp

def lastPos(node):
    data = node.data
    lp = set()
    if data == EPSILON:
        return lp
    if data not in operations:
        lp.add(node.pos)
    
    if data in '*+?':
        lp = lastPos(node.Left)
    if data == '|':
        lp = lastPos(node.Left).union(lastPos(node.Right))
    if data == '.':
        if nullable(node.Right):
            lp = lastPos(node.Left).union(lastPos(node.Right))
        else:
            lp = lastPos(node.Right)

    return lp

def followPos(node):
    pass