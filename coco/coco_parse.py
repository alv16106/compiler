from common import *
from scanner import Token


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
            print("ERRORRRRRRRR")


    def sim_set(self):
        s = set()
        # que tipo de token le sigue al igual?
        if self.la.t == "ident":
            self.move()
            n = self.characters[self.token.val]
            if not n:
                print("Set indefinido '", self.token.val, "'")
            s.update(n)
        elif self.la.t == "string":
            self.move()
            s.update(set(self.token.val[1:-1]))
        elif self.la.t == "chr":
            self.move()
            s.add(self.token.val[1:-1])
        else:
            print("CHARACTER SET mal hecho")
        
        self.expect(".")
        return s

    def get_set(self):
        s = set()
        # primero vemos si el proximo token es un identificador
        self.expect("ident")
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.characters:
            print("duplicado alv")
        #necesitamos un =
        self.expect("=")

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
        self.expect("ident")
        name = self.token.val
        # verificamos que no sea repetido
        if name in self.keywords:
            print("duplicado alv")

        # necesitamos un =
        self.expect("=")

        # necesitamos que lo proximo sea un string
        self.expect("string")

        self.keywords[name] = self.token.val


    def parse(self):
        mode = 0
        self.la = Token(None, None, None)
        self.move()
        while 1:
            if self.la.t in self.headers:
                mode = self.la.value
                continue
            if mode == "CHARACTERS":
                self.move()
                while self.la.t == "ident":
                    self.get_set()
            elif mode == "KEYWORDS":
                self.move()
                while self.la.t == "ident":
                    self.get_keyword()
            elif mode == "TOKENS":
                pass
