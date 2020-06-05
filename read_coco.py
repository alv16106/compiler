import enum
from coco.coco_parse import Coco, machines, CocoParser
from coco.common import get_ident, get_keyword
from coco.automatonTools import ScannerTable
from coco.scanner import Token, Scanner
from coco.Node import get_productions


def get_file(filename):
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content


if __name__ == "__main__":
    f = input('Name of source file: ')
    buffer = get_file(f)
    vocab = set()

    # Add all tokens to dict
    for c in machines:
        machines[c].name = c
        vocab.update(machines[c].transition_table()[-1])
    
    table = ScannerTable(vocab=vocab)
    table.build(machines.values())

    scanner = Scanner(buffer, table, Coco.EOF)

    parser = CocoParser(scanner)

    name, k, c, t, p = parser.parse()
    print(name)

    print(c)

    # FOR new language
    new_machines = {}

    for key in k:
        new_machines[key] = get_keyword(k[key])


    new_machines.update(t)
    vocab2 = set()

    Enumerator = enum.Enum(name, list(new_machines.keys()))

    # Add all tokens to dict
    for c in new_machines:
        print(c)
        new_machines[c].name = Enumerator[c]
        vocab.update(new_machines[c].transition_table()[-1])
        
    table = ScannerTable(vocab=vocab)
    table.build(new_machines.values())

    get_productions('./parsers/'+ name + '.py', p)

    while 1:
        buffer = input()

        scanner = Scanner(buffer, table, Coco.EOF)
        t = scanner.get_token()
        print(t)

        while t.t != Coco.EOF:
            t = scanner.get_token()
            print(t)

        scanner.scanTable.reset()
