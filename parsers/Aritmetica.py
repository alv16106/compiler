Expr():
    while self.la.t == fist:
        Stat()
        if self.la.t == ";":
            self.expect(";")
    if self.la.t == ".":
        self.expect(".")


Stat():
    value=Expression()
    print(value)


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
        signo = -1
    if self.la.t == white:
        result=Number()
    if self.la.t == white:
        if self.la.t == "(":
            self.expect("(")
        result=Expression()
        if self.la.t == ")":
            self.expect(")")
    result*=signo
    return result


Number():
    self.expect(number)
     result = int(self.t.val)
    return result
