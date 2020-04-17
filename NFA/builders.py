from .constants import *
from .state import State
from .nfa import NFA


# single symbol accepting nfa
def char(symbol):
    s0 = State()
    s1 = State(accepting=True)
    s0.addTransition(symbol, s1)
    return NFA(start=s0, end=s1)


# epsilon accepting nfa
def epsilon():
    return char(EPSILON)


# def concatenation between 2 nfas. nfa.nfa
def concat(n1, n2):
    n1.end.accepting = False
    n1.end.addTransition(EPSILON, n2.start)
    return NFA(n1.start, n2.end)


# def nfa | nfa
def selection(n1, n2):
    new_in = State()
    new_out = State()

    new_in.addTransition(EPSILON, n1.start)
    new_in.addTransition(EPSILON, n2.start)
    n1.end.addTransition(EPSILON, new_out)
    n2.end.addTransition(EPSILON, new_out)

    n2.end.accepting = False
    n1.end.accepting = False
    new_out.accepting = True

    return NFA(new_in, new_out)


def multipleSelection(machines):
    new_in = State()

    for n in machines:
        new_in.addTransition(EPSILON, n.start)
        n.end.pertenency = n.name

    return NFA(new_in, n.end)


# def Kleene nfa*
def star(n1):
    n1.start.addTransition(EPSILON, n1.end)
    n1.end.addTransition(EPSILON, n1.start)
    return NFA(n1.start, n1.end)


# def + nfa+
def plus(n1):
    n1.end.addTransition(EPSILON, n1.start)
    return n1


# def symbol? == symbol | EPSILON
def question(n1):
    n1.start.addTransition(EPSILON, n1.end)
    return n1
