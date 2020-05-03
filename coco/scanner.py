
class Token:
    def __init__(self, t, val, pos):
        self.t = t
        self.val = val
        self.pos = pos
    
    def __str__(self):
        values = (self.t.name, self.val, self.pos)
        return 'Token of type "\033[1m%s\033[0m with value %s in position %s' % values

class Scanner:
    def __init__(self, s, table, EOF):
        self.buf = s
        self.bufLen = len(s)
        self.pos = 0
        self.lines = s.splitlines()
        self.line = 0
        self.tokens = []
        self.scanTable = table
        self.errors = []
        self.ignore = set([chr(9), chr(10), chr(13), " "])
        self.EOF = EOF


    def get_token(self):
        if self.pos >= self.bufLen:
            t = (self.EOF, "EOF", self.bufLen)
            return Token(*t)
        while self.buf[self.pos] in self.ignore:
            self.pos += 1
        accepted = []
        start = self.pos
        while True:

            if self.pos < self.bufLen:
                c = self.buf[self.pos]
                n = self.scanTable.setMove(c)
                # Move to next character        
                self.pos += 1

                # if we can continue without error
                if n:
                    #see if n is accepting
                    if n.accepting:
                        t = (n.pertenency, self.buf[start:self.pos], self.pos)
                        # we found a token, add to memory and search for more
                        if not self.scanTable.setCanMove(self.peek()):
                            token = Token(*t)
                            self.scanTable.reset()
                            self.tokens.append(token)
                            return token
                        # print('Puede haber mas')
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
                    print('error no mach nada')

            else:
                t = (self.EOF, "EOF", self.bufLen)
                return Token(*t)

    def peek(self):
        if self.pos < self.bufLen:
            return self.buf[self.pos]
        return 'EOF'            

