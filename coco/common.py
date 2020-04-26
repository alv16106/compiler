from string import ascii_letters, digits
from ..NFA.builders import char, concat, star, selection

LETTER = set(ascii_letters)
DIGIT = set(digits)
LOD = LETTER + DIGIT

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
    inside = star(char(LOD))
    return concat(quote, concat(inside, quote2))

# char   = '\'' anyButApostrophe '\''.

