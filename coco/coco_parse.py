import enum
from coco.common import get_keyword, get_ident, get_char, get_number, char, get_string, concat, selection, star, question
from coco.scanner import Token

class Coco(enum.Enum):
    Ident = 1
    Number = 2
    Char = 3
    String = 4
    Equal = 5
    Or = 6
    Finish = 7
    GroupStart = 8
    GroupEnd = 9
    OptionStart = 10
    OptionEnd = 11
    IterationStart = 12
    IterationEnd = 13
    Plus = 14
    Minus = 15
    CHARACTERS = 16
    KEYWORDS = 17
    TOKENS = 18
    COMPILER = 19
    CHR = 20
    FOLLOW = 21
    EOF = None


machines = {
    Coco.Ident: get_ident(),
    Coco.Number: get_number(),
    Coco.Char: get_char(),
    Coco.String: get_string(),
    Coco.Equal: char("="),
    Coco.Or: char("|"),
    Coco.Finish: char("."),
    Coco.GroupStart: char("("),
    Coco.GroupEnd: char(")"),
    Coco.OptionStart: char("["), 
    Coco.OptionEnd: char("]"),
    Coco.IterationStart: char("{"),
    Coco.IterationEnd: char("}"),
    Coco.Plus: char("+"),
    Coco.Minus: char("-"),
    Coco.CHR: get_keyword("CHR("),
    Coco.FOLLOW: get_keyword(".."),
    Coco.CHARACTERS: get_keyword("CHARACTERS"),
    Coco.KEYWORDS: get_keyword("KEYWORDS"),
    Coco.TOKENS: get_keyword("TOKENS"),
    Coco.COMPILER: get_keyword("COMPILER"),
}


class CocoParser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.error = 0
        self.token = None
        self.la = None
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
    

    def move(self):
        print("moving to", self.la)
        self.token = self.la
        self.la = self.scanner.get_token()
    
    def expect(self, x):
        if self.la.t == x:
            self.move()
        else:
            print("Error, expected", x)


    def sim_set(self):
        s = set()
        # que tipo de token le sigue al igual?
        if self.la.t == Coco.Ident:
            self.move()
            n = self.characters[self.token.val]
            if not n:
                print("Set indefinido '", self.token.val, "'")
            s.update(n)
        elif self.la.t == Coco.String:
            self.move()
            s.update(set(self.token.val[1:-1]))
        elif self.la.t == Coco.Char:
            print('enter char')
            self.move()
            v1 = self.token.val[1:-1]
            s.add(v1)
            if self.la.t == Coco.FOLLOW:
                self.move()
                self.expect(Coco.Char)
                v2 = self.token.val[1:-1]
                for i in range( ord(v1), ord(v2) + 1 ):
                    s.add(chr(i))

        elif self.la.t == Coco.CHR:
            self.move()
            self.expect(Coco.Number)
            s.update(chr(int(self.token.val)))
            self.expect(Coco.GroupEnd)
        else:
            print("CHARACTER SET mal hecho")
        
        self.expect(Coco.Finish)
        return s

    def get_set(self):
        s = set()
        # primero vemos si el proximo token es un identificador
        self.expect(Coco.Ident)
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.characters:
            print("duplicado alv")
        #necesitamos un =
        self.expect(Coco.Equal)

        s = self.sim_set()
        
        # hay mas?
        while self.la.t == Coco.Plus or self.la.t == Coco.Minus:
            if self.la.t == Coco.Plus:
                self.move()
                s2 = self.sim_set()
                s.update(s2)
            else:
                self.move()
                s2 = self.sim_set()
                s.update(s2)
 
        self.characters[name] = s
    
    def get_keyword(self):
        self.expect(Coco.Ident)
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.keywords:
            print("duplicado alv")

        # necesitamos un =
        self.expect(Coco.Equal)

        # necesitamos que lo proximo sea un string
        self.expect(Coco.String)

        self.keywords[name] = self.token.val[1:-1]

        self.expect(Coco.Finish)


    def get_token(self):
        self.expect(Coco.Ident)
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.tokens:
            print("duplicado alv")
        
        # necesitamos un =
        self.expect(Coco.Equal)

        t = self.get_token_part()
        self.tokens[name] = t

        self.expect(Coco.Finish)
    
    def get_token_part(self):
        
        t = self.get_term()

        # Repetimos mientras el siguiente siga siento un Or
        while self.la.t == Coco.Or:
            self.move()
            t2 = self.get_term()
            t = selection(t, t2)
        return t

    def get_term(self):
        terminators = [Coco.GroupEnd, Coco.IterationEnd, Coco.OptionEnd, Coco.Or]
        t = self.get_factor()
        while self.la.t != Coco.Finish and self.la.t not in terminators:
            t2 = self.get_factor()
            t = concat(t, t2)
        return t

    
    def get_factor(self):
        machine = None
        print("EN GET FACTOR", self.la.t)
        # Que es lo proximo?
        if self.la.t == Coco.Ident:
            self.move()
            ID = self.token.val
            value = ''
            # search if its keyword or character
            if ID in self.keywords:
                value = self.keywords[ID]
                machine = get_keyword(value)
            elif ID in self.characters:
                value = self.characters[ID]
                machine = char(value)
            else:
                print("No existe tal identifier")
        
        elif self.la.t == Coco.String:
            self.move()
            machine = get_keyword(self.token.val[1:-1])
        
        elif self.la.t == Coco.String:
            self.move()
            machine = char(self.token.val[1:-1])
            
        # parentesis start
        elif self.la.t == Coco.GroupStart:
            self.move()
            machine = self.get_token_part()
            self.expect(Coco.GroupEnd)
            
        # repeticion start
        elif self.la.t == Coco.IterationStart:
            self.move()
            m = self.get_token_part()
            machine = star(m)
            self.expect(Coco.IterationEnd)

        # opcion start
        elif self.la.t == Coco.OptionStart:
            self.move()
            m = self.get_token_part()
            machine = question(m)
            self.expect(Coco.IterationEnd)

        # ninguno, por lo tanto error
        else:
            print("Error en la creacion del token")

        return machine


    def parse(self):
        self.la = Token(Coco.CHARACTERS, None, None)
        self.move()
        self.expect(Coco.COMPILER)
        self.expect(Coco.Ident)

        name = self.token.val

        while 1:
            if self.la.t == Coco.CHARACTERS:
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_set()
            elif self.la.t == Coco.KEYWORDS:
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_keyword()
            elif self.la.t == Coco.TOKENS:
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_token()
                break
        return name, self.keywords, self.characters, self.tokens
