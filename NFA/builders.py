from constants import *
from state import State
from nfa import NFA

def char(symbol):
    s0 = State()
    s1 = State(accepting=True)
    s0.addTransition(symbol, s1)
    return NFA(s0, s1)


def epsilon():
    return char(EPSILON)


def concat(n1, n2):
    n1.end.accepting = False
    n1.end.addTransition(EPSILON, n2.start)
    return NFA(n1.start, n2.end)


def selection(n1, n2):
    new_in = State()
    new_out = State()

    new_in.addTransition(EPSILON, n1.start)
    new_in.addTransition(EPSILON, n2.start)
    n1.out.addTransition(EPSILON, new_out)
    n2.out.addTransition(EPSILON, new_out)

    n2.out.accepting = False
    n1.out.accepting = False
    new_out.accepting = True

    return NFA(new_in, new_out)


def star(n1):
    pass

def plus(n1):
    pass
