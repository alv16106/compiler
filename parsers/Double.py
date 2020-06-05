Expr():
    while self.la.t == fist:
        Stat()
        if self.la.t == ";":
            self.expect(";")
        while self.la.t == fist:
            self.expect(white)
    while self.la.t == fist:
        self.expect(white)
    if self.la.t == ".":
        self.expect(".")


Stat():
    value=Expression()
    System.Console.WriteLine("Resultado: {0}",value)


Expression():
    result1=Term()
    while self.la.t == fist:
        if self.la.t == white:
            if self.la.t == "+":
                self.expect("+")
            result2=Term()
            result1+=result2
        if self.la.t == white:
            if self.la.t == "-":
                self.expect("-")
            result2=Term()
            result1-=result2
    result=result1
    return result


Term():
    result1=Factor()
    while self.la.t == fist:
        if self.la.t == white:
            if self.la.t == "*":
                self.expect("*")
            result2=Factor()
            result1*=result2
        if self.la.t == white:
            if self.la.t == "/":
                self.expect("/")
            result2=Factor()
            result1/=result2
    result=result1
    return result


Factor():
    if self.la.t == fist:
        if self.la.t == "-":
            self.expect("-")
        sign = -1
    if self.la.t == white:
        result=Number()
    if self.la.t == white:
        if self.la.t == "(":
            self.expect("(")
        result=Expression()
        if self.la.t == ")":
            self.expect(")")
    result*=sign
    return result


Number():
    if self.la.t == white:
        self.expect(number)
    if self.la.t == white:
        self.expect(decnumber)
    result = float(self.token.val)
    return result


