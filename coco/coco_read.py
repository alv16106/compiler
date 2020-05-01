import enum
from coco.common import get_char, get_ident, get_number, get_keyword
from coco.scanner import Token, Scanner, ScannerTable


def get_file(filename):
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content


if __name__ == "__main__":
    buffer = get_file('test.txt')
    headers = set()
    vocab = set()
    headers.add(get_keyword('CHARACTERS'))
    headers.add(get_keyword('KEYWORDS'))
    headers.add(get_keyword('TOKENS'))

    # Add letters on headers to vocab
    for h in headers:
        vocab.update(h.transition_table()[-1])

    # Add all tokens to dict
    for c in Coco:
        v = c.value
        if v is str:
            vocab.update(v)
            continue
        vocab.update(v().transition_table()[-1])
    
    table = ScannerTable(vocab=vocab)