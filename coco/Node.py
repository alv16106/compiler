class Node:
    def __init__(self, type, value, args=None, n=None, prev=None):
        self.type = type
        self.value = value
        self.args = args
        self.next = n
        self.previous = prev
    
    def addNext(self, n):
        self.next = n
        self.next.previous = self
    
    def prepend(self, n):
        first = self.getRoot()
        n.addNext(first)

    def append(self, n):
        last = self.getLast()
        last.addNext(n)
    
    def move(self):
        return self.next

    def getRoot(self):
        root = self
        while root.previous:
            root = root.previous
        return root
    
    def getLast(self):
        last = self
        while last.next:
            last = last.next
        return last

def convert(parent, i=2, fd=None):
    indent = 0
    hasReturn = parent['return']
    n = parent['list']
    fd.write(parent['name'] + "():\n")
    indent += i
    while n:
        if n.type == 'literal':
            fd.write(indent*' ' + 'self.expect('+ n.value +')\n')
        elif n.type == 'sem_action':
            fd.write(indent*' ' + n.value + '\n')
        elif n.type == 'op_start':
            fd.write(indent*' ' + n.value + ' ' + n.args + ':\n')
            indent += i
        elif n.type == 'op_end':
            indent -= i
        elif n.type == 'call':
            fd.write(indent*' ')
            if n.args:
                fd.write(n.args + '=')
            fd.write(n.value + '()\n')
        n = n.move()
    
    if hasReturn:
        fd.write(indent*' ' + 'return ' + hasReturn + 3*'\n')
    else:
        fd.write(2*'\n')


def get_productions(fname, productions):
    f = open(fname, 'w+')
    for p in productions.values():
        convert(p, 4, f)
    f.close()

def compute_first(productions):
    first = {}
    for prod in productions:
        if prod in first:
            continue

        first[prod] = set()
        n = prod['list']
        while True:
            if n.type == 'literal':
                first[prod].add(n.value)
                break
            elif n.type == 'sem_action':
                break
            elif n.type == 'op_start' and n.value == 'if':
                pass
            elif n.type == 'op_end':
                pass
            elif n.type == 'call':
                pass

if __name__ == "__main__":
    test = {'return': 'test', 'name': 'Test'}
    s0 = Node('op_start', 'while', args='self.la.t==any')
    s1 = Node('call', 'Stat', 'test')
    s2 = Node('literal', ';')
    s3 = Node('op_start', 'while', args='self.la.t==white')
    s4 = Node('literal', 'white')
    s5 = Node('op_end', None)
    s6 = Node('op_end', None)
    s7 = Node('literal', '.')
    s0.addNext(s1)
    s1.addNext(s2)
    s2.addNext(s3)
    s3.addNext(s4)
    s4.addNext(s5)
    s5.addNext(s6)
    s6.addNext(s7)
    test['list'] = s0
    convert(test)