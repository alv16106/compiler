import enum
from coco.coco_parse import Coco, machines, CocoParser
from coco.common import get_ident
from coco.scanner import Token, Scanner, ScannerTable


def get_file(filename):
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content


if __name__ == "__main__":
    buffer = get_file('coco/example.txt')
    headers = set()
    vocab = set()

    # Add all tokens to dict
    for c in machines:
        machines[c].name = c
        vocab.update(machines[c].transition_table()[-1])
    
    table = ScannerTable(vocab=vocab)
    table.build(machines.values())

    scanner = Scanner(buffer, table)

    while 1:
        t = scanner.get_token()
        print(t)