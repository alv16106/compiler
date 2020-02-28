symbols = '*/+-'

def analize(s):
    ops = []
    numbers = []
    last = ''
    for c in s:
        if c in symbols:
            ops.append(c)
        else:
            if last.isdigit():
                numbers[-1] = numbers[-1] + c
            else:
                numbers.append(c)
        last = c
    numbers = [int(n) for n in numbers]
    return ops, numbers

def operate(n1, n2, op):
    if op == '*':
        return n1 * n2
    elif op == '/':
        return n1 / n2
    if op == '+':
        return n1 + n2
    return n1 - n2


def evaluate(s):
    while '(' in s:
        sub = s[s.find('(')+1:s.rfind(')')]
        temp_value = evaluate(sub)
        s = s.replace('('+ sub + ')', str(temp_value))
    ops, values = analize(s)
    for symbol in symbols:
        while symbol in ops:
            oi = ops.index(symbol)
            result = operate(values[oi], values[oi+1], symbol)
            del values[oi:oi+2]
            del ops[oi]
            values.insert(oi, result)
    return values[0]


if __name__ == "__main__":
    string = input('Ingrese su cadena: ')
    print(evaluate(string))