class Quadruple:
    def __init__(self, operation_I, dir1_I=None, dir2_I=None, dir3_I=None):
        self.operation = operation_I
        self.dir1 = dir1_I
        self.dir2 = dir2_I
        self.dir3 = dir3_I

    def __repr__(self):
        return str(self.__dict__)
