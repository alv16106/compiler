from string import ascii_letters, digits, printable
from NFA.builders import char, concat, star, selection, question

LETTER = set(ascii_letters)
DIGIT = set(digits)
LOD = LETTER.union(DIGIT)
ANY = set(printable) - set("\n\r")
ANYBUTQUOTE = ANY.difference(set('"'))
ANYBUTSINGLEQUOTE = ANY.difference(set("'"))

# ident  = letter {letter | digit}.
def get_ident():
    lmachine = char(LETTER)
    lodmachine = char(LOD)
    return concat(lmachine, star(lodmachine))


# number = digit {digit}. 
def get_number():
    dmachine = char(DIGIT)
    dmachine2 = char(DIGIT)
    return concat(dmachine, star(dmachine2))


# string = '"' {anyButQuote} '"'. 
def get_string():
    quote = char('"')
    quote2 = char('"')
    inside = star(char(ANYBUTQUOTE))
    return concat(quote, concat(inside, quote2))


# char   = '\'' anyButApostrophe '\''.
def get_char():
    quote = char("'")
    quote2 = char("'")
    inside = char(ANYBUTSINGLEQUOTE)
    return concat(quote, concat(inside, quote2))


# for keywords
def get_keyword(s):
    machine = char(s[0])
    for a in s[1:]:
        machine = concat(machine, char(a))
    return machine