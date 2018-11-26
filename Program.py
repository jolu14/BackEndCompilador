
import TokensCodes
import SemanticCube
import Quadruple

class Program:
    expStack = []
    opStack = []
    typesStack = []



    def __init__(self):
        self.currentContext = ['global']
        self.funcsDir = {'global': Function('global', 'global', -1)}
        self.cuadruplos = []
        self.temps = 1
        self.arrTemps = []
        self.ifjumps = []
        self.startWhiles = []
        self.whilejumps = []
        self.paramsize = 0
        self.paramsstack = []
        self.lastfuncpos = -1
        self.limits = []
        self.llamadasPend = []
        self.ins = 1
        self.pends = []

    def getTempMemory(self):
        return self.funcsDir[self.getCurrentContext()].getTemp()

    def getConstMemory(self, value,type):
        return self.funcsDir[self.getCurrentContext()].addConst(value,type)

    def generateMainJump(self):
        self.cuadruplos.append(["goto","","",""])

    def generateIFJump(self,goto,v):
        self.ifjumps.append(len(self.cuadruplos))
        self.cuadruplos.append([goto,v,"",""])

    def startWhile(self):
        self.startWhiles.append(len(self.cuadruplos))

    def generateWHILEJump(self,goto, v):
        self.whilejumps.append(len(self.cuadruplos))
        self.cuadruplos.append([goto,v,"",""])

    def fillWHILEJump(self):
        self.cuadruplos[self.whilejumps.pop()][3] = len(self.cuadruplos)

    def endWHILE(self):
        self.cuadruplos.append(["goto","","", self.startWhiles.pop()])

    def endTRUEIF(self):
        self.ifjumps.insert(0,len(self.cuadruplos))
        self.cuadruplos.append(["goto","","",""])

    def fillIFJump(self):
        self.cuadruplos[self.ifjumps.pop()][3] = len(self.cuadruplos)

    def setMainPosition(self):
        self.cuadruplos[0][3] = len(self.cuadruplos)

    def addFunc(self, func_name, func_type=None):
        if func_name in self.funcsDir:
            return Response(False, "Function redefinition")
        if func_type == None:
            func_type = self.getLastFoundType()
        self.funcsDir[func_name] = Function(func_name, func_type, len(self.cuadruplos))
        self.currentContext.append(func_name)
        return Response()

    def addVariable(self, var_name, var_type=None):
        if self.isVarRedefined(var_name):
            return Response(False, "Variable redefinition")
        if var_type == None:
            var_type = self.getLastFoundType()
        self.funcsDir[self.getCurrentContext()].addVar(var_name, var_type)

        return Response()
    def getParamDir(self, var_name):
        dir = self.funcsDir[self.getCurrentContext()].getParamDir(var_name)
        return dir

    def getVarDir(self, var_name):
        dir = self.funcsDir[self.getCurrentContext()].getVarDir(var_name)
        if dir == -1:
            dir = self.funcsDir["global"].getVarDir(var_name)
        return dir

    def getVarInfo(self, dir):
        dir = self.funcsDir[self.getCurrentContext()].getVarInfo(dir)
        if dir == None:
            dir = self.funcsDir["global"].getVarInfo(dir)
        return dir

    def appendLimits(self, var_name):
        limits = self.funcsDir[self.getCurrentContext()].getVarLimits(var_name)
        if limits[0] == -1:
            limits = self.funcsDir["global"].getVarLimits(var_name)
        self.limits.extend(limits)
        #print(self.limits)

    def addArrayQuads(self, x):
        if x == 1:
            t = -1
            res = self.expStack.pop()
            #print( self.expStack)
            var_name = self.expStack.pop()
            limits = self.funcsDir[self.getCurrentContext()].getVarSize(var_name)
            if limits[0] == -1:
                limits = self.funcsDir["global"].getVarSize(var_name)
            if limits[0] != -1:
                self.expStack.append(self.getConstMemory(self.expStack.pop(), "int"))
                if limits[1] == 1:
                    t  = self.getTempMemory()
                    self.cuadruplos.append(["+",self.expStack.pop(),res, t])
                    self.expStack.append("&" + t.__str__())
                else:
                    t  = self.getTempMemory()
                    self.expStack.pop();
                    self.expStack.append(self.getConstMemory(limits[2], "int"))
                    self.cuadruplos.append(["*",self.expStack.pop(),res, t])
                    self.expStack.append(t)
        else:
            var_name = self.expStack.pop()
            t  = self.getTempMemory()
            self.cuadruplos.append(["+",self.expStack.pop(),self.expStack.pop(), t])
            t2  = self.getTempMemory()

            limits = self.funcsDir[self.getCurrentContext()].getVarSize(var_name)
            if limits[0] == -1:
                limits = self.funcsDir["global"].getVarSize(var_name)
            #print(var_name);
            #print(limits);
            self.expStack.append(self.getConstMemory(limits[3], "int"))
            self.cuadruplos.append(["+",t,self.expStack.pop(), t2])
            self.expStack.append("&"+ t2.__str__())
            #print( self.expStack)

    def addFuncParam(self, var_name, var_type=None):
        if var_type == None:
            var_type = self.getLastFoundType()
        self.funcsDir[self.getCurrentContext()].addParam(var_name, var_type)
        return Response()

    def getCurrentContext(self):
        return self.currentContext[len(self.currentContext) - 1]

    def popContext(self):
        self.currentContext.pop();

    def typeFound(self, type_found):
        Program.typesStack.append(type_found)

    def getLastFoundType(self):
        return Program.typesStack.pop()

    def isVarRedefined(self, var_name):
        if any(d.name == var_name for d in self.funcsDir[self.getCurrentContext()].vars) \
        or any(d.name == var_name for d in self.funcsDir[self.getCurrentContext()].params):
            return True
        else:
            return False

    def popexp1(self):
        if len(Program.opStack) > 0:
            lop = Program.opStack[len(Program.opStack) - 1]
            if  lop == '/' or \
                lop == '*' :
                Program.expStack.append(Program.opStack.pop())

    def popexp2(self):
        if len(Program.opStack) > 0:
            lop = Program.opStack[len(Program.opStack) - 1]
            if  lop == '+' or \
                lop == '-':
                Program.expStack.append(Program.opStack.pop())

    def popexp3(self):
        if len(Program.opStack) > 0:
            lop = Program.opStack[len(Program.opStack) - 1]
            if  lop == '<' or \
                lop == '>' or \
                lop == '<=' or \
                lop == '>=' or \
                lop == '==' or \
                lop == '!=':
                Program.expStack.append(Program.opStack.pop())

    def popParent(self):
        t  = self.printExp()
        if t != "":
            self.arrTemps.append(t)
        #if len(Program.opStack) > 0:
            #if  Program.opStack[len(Program.opStack) - 1] == ')':
                #Program.opStack.pop()

    def appendOp(self, op):
        #print(self.cuadruplos)
        Program.opStack.append(op)

    def appendExp(self, exp):
        Program.expStack.append(exp)

    def printExp(self):
        #print(Program.expStack)
        t = ""
        while(len(Program.opStack) > 0):
            op = ""
            x1 = ""
            x2 = ""
            if len(Program.opStack) > 0:
                op = Program.opStack.pop()

            if len(self.arrTemps) > 0:
                x2 = self.arrTemps.pop()
            elif len(Program.expStack) > 0:
                x2 = Program.expStack.pop()

            if len(self.arrTemps) > 0:
                x1 = self.arrTemps.pop()
            elif len(Program.expStack) > 0:
                x1 = Program.expStack.pop()
            t  = self.getTempMemory()
            self.cuadruplos.append([op,x1,x2, t])
            self.arrTemps.append(t)
            self.temps = self.temps + 1
        self.arrTemps = []
        return t

    def assignLast(self):
        #print(Program.expStack)
        op = Program.opStack.pop()
        x1 = Program.expStack.pop()
        x2 = Program.expStack.pop()

        self.cuadruplos.append([op,x1,"", x2])


    def __repr__(self):
        return str(self.__dict__)

    def prepareData(self):
        data = {'funcs': [], 'cuadruplos':[] }

        funcs  = []
        for quad in self.cuadruplos:
            quad[0] = self.operations[quad[0]]

        for f in self.funcsDir:
            f = self.funcsDir[f]
            funcs.append({'name': f.name, 'CSTART': f.CSTART,\
            'TSTART': f.TSTART, 'VSTART':f.VSTART,  \
            'CMEMORY': f.memory_cosnt, 'TMEMORY': f.memory_temps,  \
            'VMEMORY': f.memory_vars} )

        data['cuadruplos'] = self.cuadruplos
        data['funcs'] = funcs

        return data


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
        'gotoF': 12,
        'gotot': 13,
        'gosub': 14,
        'param': 15,
        'return': 16,
        'endfunc': 17,
        'era': 18,
        'print': 19,
        'read': 20,
        'and': 21,
        'or': 22,
        'endprog': 23,
        'endfunc': 24,
        'ver':25,
        '<=':26,
        '>=':27
    }

# ==============================================================================
class Function:
    def __init__(self, name_I, type_I, pos):
        self.name = name_I
        self.type = type_I
        self.vars = []
        self.params = []
        self.pos = pos

        self.memory_cosnt = []
        self.memory_vars = []
        self.memory_temps = []
        self.CSTART = 0
        self.const_start = 0
        self.TSTART = 500
        self.temps_start = 500
        self.VSTART = 3000
        self.vars_start = 3000

        if self.name == "global":
            self.CSTART = 5000
            self.const_start = 5000
            self.TSTART = 5500
            self.temps_start = 5500
            self.VSTART = 8000
            self.vars_start = 8000

    def addConst(self,value,type):
        self.memory_cosnt.append([value,type])
        self.const_start = self.const_start + 1
        return self.const_start - 1

    def getTemp(self):
        self.memory_temps.append([None])
        self.temps_start = self.temps_start + 1
        return self.temps_start - 1

    def addVar(self,var_name,var_type,sizeX=1,sizeY=1):
        types = var_type.split(" ");
        st = self.vars_start
        dims = 0
        if (len(types) > 1 and types[0][:5] == 'lista'):
            sizeX = int(types[0][5:])
            dims = dims + 1

        if (len(types) > 2 and types[1][:5] == 'lista'):
            sizeY = int(types[1][5:])
            dims = dims + 1

        l = [[None, types[len(types) - 1]]] * (sizeX * sizeY)
        self.memory_vars.extend(l)
        self.vars_start = self.vars_start + (sizeX * sizeY)

        self.vars.append(Var(var_name,types[len(types) - 1],st,sizeX,sizeY,dims))
        return st

    def addParam(self,var_name,var_type,sizeX=1,sizeY=1):
        types = var_type.split(" ");
        st = self.vars_start
        dims = 0
        if (len(types) > 1 and types[0][:5] == 'lista'):
            sizeX = int(types[0][5:])
            dims = dims + 1

        if (len(types) > 2 and types[1][:5] == 'lista'):
            sizeY = int(types[1][5:])
            dims = dims + 1
        l = [[None,types[len(types) - 1]]] * (sizeX * sizeY)
        self.memory_vars.extend(l)
        self.vars_start = self.vars_start + (sizeX * sizeY)

        self.params.append(Var(var_name,types[len(types) - 1],st,sizeX,sizeY,dims))
        return st



    def __repr__(self):
        return str(self.__dict__)

    def getVarDir(self, var_name):
        for v in self.vars:
            if v.name == var_name:
                return v.dir

        for v in self.params:
            if v.name == var_name:
                return v.dir

        return -1

    def getVarInfo(self, dir):
        for v in self.vars:
            if v.dir == dir:
                return v

        for v in self.params:
            if v.dir == dir:
                return v
        return None

    def getVarLimits(self,var_name):

        for v in self.vars:
            #print(v.name)
            if v.name == var_name:
                if v.dims > 1:
                    return [v.x,v.y]
                else:
                    return [v.x]

        for v in self.params:
            #print(v.name)
            if v.name == var_name:
                if v.dims > 1:
                    return [v.x,v.y]
                else:
                    return [v.x]
        return [-1]

    def getVarSize(self,var_name):
        for v in self.vars:
            #print(v.name)
            if v.name == var_name:
                return [1,v.dims,v.x, v.dir ]


        for v in self.params:
            #print(v.name)
            if v.name == var_name:
                return [1,v.dims,v.x, v.dir ]
        return [-1]


    def getParamDir(self, var_name):
        for v in self.params:
            if v.name == var_name:
                return v.dir
        return -1

    def get(self):
        return self.__dict__


# ==============================================================================
class Var:
    def __init__(self, name_I, type_I, dir, x=0,y=0,dims=0):
        self.name = name_I
        self.type = type_I
        self.dir = dir
        self.x = x
        self.y = y
        self.dims = dims

    def __repr__(self):
        return str(self.__dict__)
    def get(self):
        return self.__dict__

# ==============================================================================
class Response:
    def __init__(self, success_I=True, message_I=""):
        self.success = success_I
        self.message = message_I
