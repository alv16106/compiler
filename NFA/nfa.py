class NFA:
    def __init__(self, start, end, marked=False):
        self.start = start
        self.end = end
        self.marked = marked
    
    def match(self, string):
        return self.start.matches(string, [])
    
    def __str__(self):
        return 'NFA con end: ' + str(5)