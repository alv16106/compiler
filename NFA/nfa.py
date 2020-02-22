class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def match(self, string):
        return self.start.matches(string)