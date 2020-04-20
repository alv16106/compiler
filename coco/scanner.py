from coco.automatonTools import ScannerTable

class Token:
    def __init__(self, t, val, pos):
        self.t = t
        self.val = val
        self.pos = pos
    
    def __str__(self):
        values = (self.t.name, self.val, self.pos)
        return 'Token of type %s with value %s in position %s' % values

class Scanner:
    def __init__(self, s, table):
        self.buf = s
        self.bufLen = len(s)
        self.pos = 0
        self.lines = s.splitlines()
        self.tokens = []
        self.scanTable = table
        self.errors = []


    def get_token(self):
        accepted = []
        start = self.pos
        while True:

            if self.pos < self.bufLen:
                c = self.buf[self.pos]
                n = self.scanTable.move(c)
                # Move to next character        
                self.pos += 1

                # if we can continue without error
                if n:
                    #see if n is accepting
                    if n.accepting:
                        t = (n.pertenency, self.buf[start:self.pos], self.pos)
                        # we found a token, add to memory and search for more
                        if not self.scanTable.canMove(self.peek()):
                            print('Found token from %d to %d' % (start, self.pos))
                            token = Token(*t)
                            self.scanTable.reset()
                            self.tokens.append(token)
                            return token
                        accepted.append((n.pertenency, self.buf[start:self.pos], self.pos))
                else:
                    # if we already had an acceptance state before, rollback
                    if accepted:
                        token = Token(*accepted.pop())
                        self.scanTable.reset()
                        self.pos = token.pos
                        self.tokens.append(token)
                        return token
                    self.errors.append('Error en pos: %d' % self.pos)

            else:
                return 'EOF'

    def peek(self):
        return self.buf[self.pos + 1]                

