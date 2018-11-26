class TokensCodes:
    operations = {
        '=': 0,
        '+': 1,
        '-': 2,
        '*': 3,
        '/': 4,
        '+=': 5,
        '-=': 6,
        '>': 7,
        '<': 8,
        '==': 9,
        '!=': 10,
        'goto': 11,
        'gotof': 12,
        'gotot': 13,
        'gotosub': 14,
        'param': 15,
        'return': 16,
        'endfunc': 17,
        'era': 18,
        'print': 19,
        'read': 20
    }

    def __init__(self):
        self.x = ""

    dataTypes = {
    	'int': 0,
    	'float': 1,
    	'lista': 2,
    	'bool': 3,
    	'texto': 4,
        'NOTDEFINDED':99
    }
