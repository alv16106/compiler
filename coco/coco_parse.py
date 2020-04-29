import enum
from tree import Node
from utils import print2D
from common import *
from scanner import Token


class Coco(enum.Enum):
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
        pStack = []
        eTree = Node()
        pStack.append(eTree)
        currentTree = eTree
        self.expect(Coco.Ident)
        name = self.token.val

        # verificamos que no sea repetido
        if name in self.tokens:
            print("duplicado alv")
        
        # necesitamos un =
        self.expect(Coco.Equal)

        # Que es lo proximo?
        while self.la.t != Coco.Finish:
            # operacion |
            if self.la.t == Coco.Or:
                self.move()
                currentTree.data = "|"
                currentTree.right = Node()
                pStack.append(currentTree)
                currentTree = currentTree.right

            elif self.la.t == Coco.Ident:
                self.move()
                ID = self.token.val
                value = ''
                # search if its keyword or character
                if ID in self.keywords:
                    value = self.keywords[ID]
                elif ID in self.characters:
                    value = self.characters[ID]
                else:
                    print("No existe tal identifier")
                
                # modify stack
                currentTree.data = value
                parent = pStack.pop()
                currentTree = parent
            
            # parentesis start
            elif self.la.t == Coco.GroupStart:
                self.move()
                currentTree.left = Node()
                pStack.append(currentTree)
                currentTree = currentTree.left
            
            # parentesis end
            elif self.la.t == Coco.GroupEnd:
                self.move()
                currentTree = pStack.pop()
            
            # repeticion start
            elif self.la.t == Coco.IterationStart:
                self.move()
                currentTree.left = Node()
                pStack.append(currentTree)
                currentTree = currentTree.left

            # repeticion end
            elif self.la.t == Coco.IterationEnd:
                self.move()
                pass

            # opcion start
            elif self.la.t == Coco.OptionStart:
                self.move()
                pass

            # opcion end
            elif self.la.t == Coco.OptionEnd:
                self.move()
                pass

            # ninguno, por lo tanto error
            else:
                pass



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
