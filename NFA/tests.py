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

    """ k = star(a)
    print('Kleen tests: ')
    print('Positive:', k.match('a'))
    print('Positive:', k.match(''))
    print('Positive:', k.match('aaaaa'))
    print('Negative:', k.match('ab')) """

    """ p = plus(a)
    print('Plus tests: ')
    print('Positive:', p.match('a'))
    print('Positive:', p.match('aaaaa'))
    print('Negative:', p.match(''))
    print('Negative:', p.match('ab')) """

    aorb = selection(a, b)
    p = plus(aorb)
    print('Combine tests: ')
    print('Positive:', p.match('a'))
    print('Positive:', p.match('b'))
    print('Positive:', p.match('aaaa'))
    print('Positive:', p.match('bbbb'))
    print('Positive:', p.match('ab'))
    print('Negative:', p.match(''))