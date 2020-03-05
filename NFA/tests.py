from builders import *
from state import State
from constants import EPSILON

if __name__ == "__main__":
    a = char('a')
    b = char('b')
    eps = epsilon()

    """ print('Single character tests: ')
    print('Positive:', a.match('a'))
    print('Negative:', a.match('b')) """

    """ aandb = concat(a, b)
    print('Concat tests: ')
    print('Positive:', aandb.match('ab'))
    print('Negative:', aandb.match('b')) """

    """ aorb = selection(a, b)
    print('Or tests: ')
    print('Positive:', aorb.match('b'))
    print('Positive:', aorb.match('a'))
    print('Negative:', aorb.match('ab')) """

    k = star(a)
    k.start.name = 'S0'
    k.end.name = 'S1'
    print(k.end.accepting)
    print('Kleen tests: ')
    print('Positive:', k.match('a'))
    print('Positive:', k.match(''))
    print('Positive:', k.match('aaaaa'))
    print('Negative:', k.match('ab'))