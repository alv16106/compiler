import enum
from coco.common import get_keyword, get_ident, get_char, get_number, char, get_string, concat, selection, star, question
from coco.scanner import Token


""" class Coco(enum.Enum):
    EOF = 0
    Ident = get_ident
    Number = get_number
    Char = get_char
    String = get_string
    Equal = lambda: char("=")
    Or = lambda: char("|")
    Finish = lambda: char(".")
    GroupStart = lambda: char("(")
    GroupEnd = lambda: char(")")
    OptionStart = lambda: char("[") 
    OptionEnd = lambda: char("]")
    IterationStart = lambda: char("{")
    IterationEnd = lambda: char("}")
    CHARACTERS = lambda: get_keyword("CHARACTERS")
    KEYWORDS = lambda: get_keyword("KEYWORDS")
    TOKENS = lambda: get_keyword("TOKENS")
    COMPILER = lambda: get_keyword("COMPILER") """

class Coco(enum.Enum):
    EOF = 0
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
    CHARACTERS = 14
    KEYWORDS = 15
    TOKENS = 16
    COMPILER = 17


class CocoParser:
    def __init__(self, scanner, headers):
        self.scanner = scanner
        self.headers = headers
        self.error = 0
        self.token = None
        self.la = None
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
    

    def move(self):
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
            self.move()
            s.add(self.token.val[1:-1])
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

        self.sim_set()
        
        # hay mas?
        while self.la.t == "+" or self.la.t == "-":
            if self.la.t == "+":
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

        self.keywords[name] = self.token.val
    
    def get_token(self):
        self.expect(Coco.Ident)
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.tokens:
            print("duplicado alv")
        
        # necesitamos un =
        self.expect(Coco.Equal)
        
        t = self.get_term()

        # Repetimos mientras el siguiente siga siento un Or
        while self.la.t == Coco.Or:
            t2 = self.get_term()
            t = selection(t, t2)
        return t

    def get_term(self):
        terminators = [Coco.GroupEnd, Coco.IterationEnd, Coco.OptionEnd, Coco.Or]
        t = self.get_factor()
        while self.la.t != Coco.Finish and self.token.t not in terminators:
            t2 = self.get_factor()
            t = concat(t, t2)
        return t

    
    def get_factor(self):
        machine = None

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
            machine = self.get_token()
            self.expect(Coco.GroupEnd)
            
        # repeticion start
        elif self.la.t == Coco.IterationStart:
            self.move()
            m = self.get_token()
            machine = star(m)
            self.expect(Coco.IterationEnd)

        # opcion start
        elif self.la.t == Coco.OptionStart:
            self.move()
            m = self.get_token()
            machine = question(m)
            self.expect(Coco.IterationEnd)

        # ninguno, por lo tanto error
        else:
            print("Error en la creacion del token")

        return machine


    def parse(self):
        mode = 0
        self.la = Token(None, None, None)
        self.move()
        self.expect(Coco.COMPILER)
        self.expect(Coco.Ident)

        name = self.token.val

        while 1:
            if self.la.t in self.headers:
                mode = self.la.value
                continue
            if mode == "CHARACTERS":
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_set()
            elif mode == "KEYWORDS":
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_keyword()
            elif mode == "TOKENS":
                self.move()
                while self.la.t == Coco.Ident:
                    self.get_token()
            return name, self.keywords, self.characters, self.tokens
