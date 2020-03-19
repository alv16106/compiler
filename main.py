from nfaFromRegex import traverse
from dfaFromRegex import build
from dfaFromNFA import getTransitionTable
from treebuilder import evaluate
from utils import print2D, graph, graphNFA, dfaToText, nfaToText
from NFA.constants import operations, EPSILON

if __name__ == "__main__":
    inp = input('Regex: ')

    #Get vocabulary
    symbols = set(inp) - set(operations) - set(EPSILON) - set('()')
    # Build both trees
    Tree, pos = evaluate(inp, 0)
    DFATree, pos1 = evaluate(inp + '.#', 0)

    print2D(Tree)

    follow = {}
    for p in range(pos1):
        follow[p+1] = set()

    nfa = traverse(Tree)
    nfa_table, accepting = nfa.transition_table()

    dfaFromNFA = getTransitionTable(nfa, symbols)
    dfaFromRegex = build(DFATree, symbols.union(set('#')), follow)

    graph(dfaFromNFA, inp + 'fromNFA')
    graph(dfaFromRegex, inp + 'fromRegex')
    graphNFA(nfa_table, accepting, inp + 'NFA')

    match = True
    while match:
        match = input('String: ')
        print(dfaFromNFA[0].matches(match, []))
        print(dfaFromRegex[0].matches(match, []))
        print(nfa.match(match))
    

    dfaToText(dfaFromNFA, symbols, inp + 'fromNFA')
    dfaToText(dfaFromRegex, symbols, inp + 'fromRegex')
    nfaToText(nfa_table, accepting, symbols, inp + 'NFA')