class NFA:
    def __init__(self, start, end, marked=False, name=None):
        self.start = start
        self.end = end
        self.marked = marked
        self.table = {}
        self.name = name
    
    def match(self, string):
        return self.start.matches(string, [])
    
    def transition_table(self):
        accepting = set()
        visited = set()
        symbols = set()

        def visit(state):
            if state in visited:
                return
            
            visited.add(state)
            state.name = len(visited)
            self.table[state.name] = {}

            if (state.accepting):
                accepting.add(state.name)
            

            transitions = state.transitions

            for symbol, symbolTransitions in transitions.items():
                combinedState = []
                symbols.add(symbol)
                for nextState in symbolTransitions:
                    visit(nextState)
                    combinedState.append(nextState.name)

                self.table[state.name][symbol] = combinedState
        
        visit(self.start)

        return self.table, accepting
            

    def __str__(self):
        return 'NFA con end: ' + str(5)