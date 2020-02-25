class Node:
    def __init__(self, father, data, op ,leafs=[None, None]):
        self.father = father
        self.leafs = leafs
        self.op = op
        self.data = data
    
    def getRoot(self):
        if not self.father:
            return self
        return self.father.getRoot()
    
    def addLeaf(self, leaf, side):
        self.leafs[side] = leaf
        return self