
import TokensCodes

class SemanticCube:
    CUBE = [
            # +
        [
        #   int  float lista texto bool texto
            [0,  1,    99,   4,    99,  4],# int
            [1,  1,    99,   4,    99,  4],# float
            [99, 99,   99,   99,   99,  99],# lista
            [99, 99,   99,   99,   3,   99],# bool
            [4,  4,    99,   4,    99,  4],# texto
        ],
            # -, *, /, +=, -=
        [
        #   int  float lista texto bool texto
            [0,  1,    99,   99,   99,  99],# int
            [1,  1,    99,   99,   99,  99],# float
            [99, 99,   99,   99,   99,  99],# lista
            [99, 99,   99,   99,   99,  99],# bool
            [99, 99,   99,   99,   99,  99],# texto,
        ],
            # >, <, ==, !=
        [
        #   int  float lista texto bool texto
            [3,  3,    99,   99,   99,  99],# int
            [3,  3,    99,   99,   99,  99],# float
            [99, 99,   99,   99,   99,  99],# lista
            [99, 99,   99,   3,    3,   99],# bool
            [99, 99,   99,   99,   3,   3],# texto,
        ],
    ]

    @staticmethod
    def verify(operation, type1, type2):
        indexOperation = Tokens.operations[operation]
        indexType1 = Tokens.dataTypes[type1]
        indexType2 = Tokens.dataTypes[type2]

        if (len(CUBE) < indexOperation and
            len(CUBE[indexType1]) < indexType1 and
            len(CUBE[indexOperation][indexType1]) < indexType2):

            if indexOperation == 0:
                return CUBE[0][Tokens.dataTypes[type1]][Tokens.dataTypes[type2]]
            elif indexOperation <= 6:
                return CUBE[1][Tokens.dataTypes[type1]][Tokens.dataTypes[type2]]
            elif indexOperation <= 10:
                return CUBE[3][Tokens.dataTypes[type1]][Tokens.dataTypes[type2]]

        return 99
