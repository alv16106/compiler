class Buffer:
    def __init__(self, s):
        self.buf = s
        self.bufLen = len(s)
        self.pos = 0
        self.lines = s.splitlines()
    
    

