import ply.lex as lex
import sys
import ply.yacc as yacc
import Program
import json
from pprint import pprint

import SemanticCube
currentProgram = Program.Program()
commaType = ""


palabrasReservadas = {
	'si' 		: 'IF',
	'sino' 		: 'ELSE',
	'program' 	: 'PROGRAM',
	'imprimir' 	: 'PRINT',
	'leer' 		: 'READ',
	'variables' : 'VAR',

	'int' 		: 'INT',
	'float' 	: 'FLOAT',
	'lista'     : 'LIST',
	'bool' 		: 'BOOL',
	'texto'		: 'STRING',

	'verdadero' : 'TRUE',
	'falso'		: 'FALSE',
	'void'		: 'VOID',
	'funciones' : 'FUN',
	'principal'	: 'MAIN',
	'ciclo'		: 'FOR',
	'regresar' 	: 'RETURN',
	'and'		: 'AND',
	'or'		: 'OR',

 }

tokens = [
	'EQUAL', 			'GREATER', 		'LESSER', 	'NOTEQUAL',
	'PLUS', 			'MINUS', 			'TIMES', 		'DIVIDE',
	'SEMICOLON', 		'COMMA', 			'COLON',
	'OPENPARENTHESIS', 	'CLOSEPARENTHESIS', 'SQUAREBOPEN',	'SQUAREBCLOSE',
	'OPENBRACKET', 		'CLOSEBRACKET', 	'ignore', 		'MOREEQUALS',
	'CTEINT', 			'CTEFLOAT',        'LESSEQUALS',	'EQUALEQUAL',
	'ID', 				'CTESTRING',  'GREATEROREQUAL', 'LESSEROREQUAL'
]

tokens += palabrasReservadas.values()

t_ignore 			= " \t"
t_GREATEROREQUAL	= r'\>\='
t_LESSEROREQUAL	    = r'\<\='
t_MOREEQUALS		= r'\+\='
t_LESSEQUALS 		= r'\-\='
t_EQUAL 			= r'\='
t_GREATER		= r'>'
t_LESSER 			= r'<'
t_EQUALEQUAL  		= r'\=\='
t_NOTEQUAL 			= r'!\='
t_PLUS 				= r'\+'
t_MINUS 			= r'\-'
t_TIMES 			= r'\*'
t_DIVIDE 			= r'/'
t_SEMICOLON 		= r'\;'
t_COMMA 			= r'\,'
t_COLON 			= r'\:'
t_OPENPARENTHESIS 	= r'\('
t_CLOSEPARENTHESIS 	= r'\)'
t_OPENBRACKET 		= r'\{'
t_CLOSEBRACKET 		= r'\}'
t_SQUAREBOPEN		= r'\['
t_SQUAREBCLOSE		= r'\]'
t_CTESTRING 		= r'\"[^\"]*\"'


def t_CTEFLOAT(t):
	r'[0-9]+\.[0-9]+'
	return t

def t_CTEINT(t):
	r'[-]?[0-9]+'
	return t

def t_ID(t):
	r'[A-Za-z][A-Za-z0-9]*'
	if t.value in palabrasReservadas:
		t.type = palabrasReservadas[t.value]
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("invalid char: '%s'" % t.value[0])
	t.lexer.skip(1)

def p_empty(p):
	'''empty : '''

def p_programa(p):
	'''
	programa : PROGRAM pn_1 ID SEMICOLON programaAuxiliar funcs programaAuxiliar1
	'''
	p[0] = "ACEPTADO\n"

def p_pn_1(p):
	'''
	pn_1 : empty
	'''
	currentProgram.generateMainJump()

def p_programaAuxiliar(p):
	'''
	programaAuxiliar : vars
	| empty
	'''
def p_programaAuxiliar1(p):
	'''
	programaAuxiliar1 : programaAuxiliar2 bloque main_end
	'''
	currentProgram.popContext()

def p_programaAuxiliar2(p):
	'''
	programaAuxiliar2 : MAIN pn_2
	'''
	currentProgram.addFunc(p[1], 'main')

def p_main_end(p):
	'''
	main_end :
	'''
	currentProgram.cuadruplos.append(["endprog","","", ""])


def p_pn_2(p):
	'''
	pn_2 : empty
	'''
	currentProgram.setMainPosition()

def p_funcs(p):
	'''
	funcs : FUN COLON funcs1
	| empty
	'''
def p_funcs1(p):
	'''
	funcs1 : tipo funcsAux1 funcs1
	| tipoVoid funcsAux1 funcs1
	| empty
	'''
	currentProgram.popContext()

def p_tipoVoid(p):
	'''
	tipoVoid : VOID
	'''
	if p[1] == 'void':
		currentProgram.typeFound(p[1])
		#print(typesStack)

def p_funcsAux1(p):
	'''
	funcsAux1 : funcsAux5 OPENPARENTHESIS funcsAux2 CLOSEPARENTHESIS bloque func_end
	'''
	#print(varsDir)

def p_func_end(p):
	'''
	func_end :
	'''
	currentProgram.cuadruplos.append(["endfunc","","", ""])

def p_funcsAux2(p):
	'''
	funcsAux2 : funcsAux3
	| empty
	'''

def p_funcsAux3(p):
	'''
	funcsAux3 : tipo ID funcsAux4
	'''
	#print(currentContext)
	r = currentProgram.addFuncParam(p[2])
	if  not r.success:
		print( r.message + ": " + p[2] + " at line " + str(p.lineno(2)))
		print(-1)
		sys.exit()

def p_funcsAux4(p):
	'''
	funcsAux4 : COMMA funcsAux3
	| empty
	'''


def p_funcsAux5(p):
	'''
	funcsAux5 : ID
	'''
	r = currentProgram.addFunc(p[1])
	if  not r.success:
		print( r.message + ": " + p[1] + " at line " + str(p.lineno(1)))
		print(-1)
		sys.exit()

def p_vars(p):
	'''
	vars : VAR COLON varsAuxiliar2 varsAuxiliar1
	'''


def p_varsAuxiliar1(p):
	'''
	varsAuxiliar1 : varsAuxiliar2 varsAuxiliar1
	| empty
	'''

def p_varsAuxiliar2(p):
	'''
	varsAuxiliar2 : tipo ID varsAuxiliar3 SEMICOLON
	'''
	commaType = currentProgram.getLastFoundType()
	r = currentProgram.addVariable(p[2], commaType)
	if  not r.success:
		print( r.message + ": " + p[2] + " at line " + str(p.lineno(2)))
		print(-1)
		sys.exit()


def p_varsAuxiliar3(p):
	'''
	varsAuxiliar3 : COMMA ID varsAuxiliar3
	| empty
	'''
	if p[1] == ',':
		r = currentProgram.addVariable(p[2], commaType)
		if  not r.success:
			print( r.message + ": " + p[2] + " at line " + str(p.lineno(2)))
			print(-1)
			sys.exit()


def p_tipo(p):
	'''
	tipo : INT
	| FLOAT
	| arreglo
	| BOOL
	| STRING
	'''
	#print(typesStack)
	if p[1] != None:
		currentProgram.typeFound(p[1])
	#print(p[1])
	#print(typesStack)

def p_bloque(p):
	'''
	bloque : OPENBRACKET bloqueAuxiliar1 bloqueAuxiliar CLOSEBRACKET
	'''

def p_bloqueAuxiliar(p):
	'''
	bloqueAuxiliar  : estatuto bloqueAuxiliar
	| empty
	'''
def p_bloqueAuxiliar1(p):
	'''
	bloqueAuxiliar1  : vars
	| empty
	'''

def p_estatuto(p):
	'''
	estatuto : asignacion SEMICOLON
	| condicion
	| escritura
	| lectura
	| ciclo
	| llamada SEMICOLON
	| incremento SEMICOLON
	| retorno
	'''

def p_retorno(p):
	'''
	retorno : RETURN retornoAux SEMICOLON
	'''
	currentProgram.cuadruplos.append(["return","","", currentProgram.expStack.pop()])



def p_retornoAux(p):
	'''
	retornoAux : var_cte
	| spcte
	| expression
	'''

def p_llamada(p):
	'''
	llamada : ID pn_llamada OPENPARENTHESIS false_bottom llamadaAux CLOSEPARENTHESIS  pn_llamada2
	'''



def p_pn_llamada(p):
	'''
	pn_llamada : empty
	'''
	currentProgram.expStack.append('retdata');
	currentProgram.ins = currentProgram.ins + 1
	currentProgram.cuadruplos.append(["era","","", p[-1]])
	currentProgram.paramsize = 0
	currentProgram.lastfunc = p[-1]
	if currentProgram.lastfunc not in currentProgram.funcsDir:
		print( "function not definded: " + currentProgram.lastfunc + " at line " + str(p.lineno(0)))
		print(-1)
		sys.exit()
	currentProgram.paramsstack = list(currentProgram.funcsDir[currentProgram.lastfunc].get()['params'])
	currentProgram.lastfuncpos = currentProgram.funcsDir[currentProgram.lastfunc].get()['pos']

def p_pn_llamada2(p):
	'''
	pn_llamada2 :
	'''
	if currentProgram.lastfunc not in currentProgram.funcsDir:
		print( "function not definded: " + currentProgram.lastfunc + " at line " + str(p.lineno(0)))

		print(-1)
		sys.exit()
	elif len(currentProgram.funcsDir[currentProgram.lastfunc].get()['params']) != currentProgram.paramsize:
		#print(currentProgram.paramsize.__str__())
		print( "incorrect params: " + currentProgram.lastfunc + " at line " + str(p.lineno(0)))
		print(-1)
		sys.exit()
	else:
		currentProgram.cuadruplos.append(["gosub","","", currentProgram.lastfuncpos])


def p_llamadaAux(p):
	'''
	llamadaAux : llamadaAux1
	| empty
	'''


def p_llamadaAux1(p):
	'''
	llamadaAux1 : expression end_par pn_llamada_param llamadaAux2
	'''
	currentProgram.paramsize =  currentProgram.paramsize + 1

def p_pn_llamada_param(p):
	'''
	pn_llamada_param :
	'''
	dir = currentProgram.paramsstack[0].get()['dir']
	currentProgram.paramsstack.pop(0)
	currentProgram.cuadruplos.append(["param",currentProgram.expStack.pop(),"", dir])


def p_llamadaAux2(p):
	'''
	llamadaAux2 : COMMA false_bottom llamadaAux1
	| empty
	'''

def p_ciclo(p):
	'''
	ciclo : FOR pn_8 OPENPARENTHESIS expression CLOSEPARENTHESIS pn_6 bloque pn_7
	'''
def p_pn_8(p):
	'''
	pn_8 : empty
	'''
	currentProgram.startWhile()

def p_pn_6(p):
	'''
	pn_6 : empty
	'''
	if len(currentProgram.expStack) == 0:
		p.error()
	currentProgram.generateWHILEJump("gotoF", currentProgram.expStack.pop())

def p_pn_7(p):
	'''
	pn_7 : empty
	'''
	currentProgram.endWHILE()
	currentProgram.fillWHILEJump()

def p_incremento(p):
	'''
	incremento : ID incremnetoAux1 expression
	'''

def p_incremnetoAux1(p):
	'''
	incremnetoAux1 : MOREEQUALS
	| LESSEQUALS
	'''

def p_asignacion(p):
	'''
	asignacion : ID pupid EQUAL asignacionAux
	| arregloVar EQUAL asignacionAux
	'''
	currentProgram.appendOp("=")
	currentProgram.assignLast()

def p_pupid(p):
	'''
	pupid :
	'''
	dir = currentProgram.getVarDir(p[-1])
	if dir == -1:
		print("var not definded: " + p[-1] + " at line " + str(p.lineno(-1)))
		print(-1)
		sys.exit()
	currentProgram.appendExp(dir)

def p_asignacionAux(p):
	'''
	asignacionAux : spcte
	| expression
	'''

def p_arreglo(p):
	'''
	arreglo : tipo SQUAREBOPEN CTEINT SQUAREBCLOSE
	'''
	currentProgram.typeFound("lista" + p[3] + " "+ currentProgram.getLastFoundType())

def p_arregloVar(p):
	'''
	arregloVar : ID getLimits false_bottom SQUAREBOPEN expression setVerData end_par SQUAREBCLOSE listaccess1
	'''

def p_setVerData(p):
	'''
	setVerData :
	'''
	varX = currentProgram.expStack.pop()
	currentProgram.cuadruplos.append(["ver",varX,0, currentProgram.limits.pop()])
	#print(currentProgram.expStack)
	currentProgram.expStack.append(p[-5])
	currentProgram.expStack.append(varX)
	currentProgram.addArrayQuads(1)

def p_getLimits(p):
	'''
	getLimits :
	'''
	dir = currentProgram.getVarDir(p[-1])
	if dir == -1:
		print("var not definded: " + p[-1] + " at line " + str(p.lineno(3)))
		print(-1)
		sys.exit()
	currentProgram.expStack.append(dir)

	currentProgram.appendLimits(p[-1])
	#print(currentProgram.expStack)



def p_setVerData1(p):
	'''
	setVerData1 :
	'''
	currentProgram.cuadruplos.append(["ver",currentProgram.expStack[len(currentProgram.expStack) - 1],0, currentProgram.limits.pop()])
	#print(currentProgram.expStack)
	currentProgram.expStack.append(p[-11])
	currentProgram.addArrayQuads(2)

def p_listaccess1(p):
	'''listaccess1 : SQUAREBOPEN false_bottom expression setVerData1 SQUAREBCLOSE end_par
					| empty '''

def p_lectura(p):
	'''
	lectura : READ OPENPARENTHESIS ID CLOSEPARENTHESIS SEMICOLON
	'''
	dir = currentProgram.getVarDir(p[3])
	if dir == -1:
		print("var not definded: " + p[3] + " at line " + str(p.lineno(3)))
		print(-1)
		sys.exit()
	currentProgram.cuadruplos.append(["read","","", dir])

def p_escritura(p):
	'''
	escritura : PRINT OPENPARENTHESIS escrituraAuxiliar1 CLOSEPARENTHESIS SEMICOLON
	'''
	#print(currentProgram.expStack)
	currentProgram.cuadruplos.append(["print","","", currentProgram.expStack.pop()])


def p_escrituraAuxiliar1(p):
	'''
	escrituraAuxiliar1 : expression
	| spcte
	'''

def p_condicion(p):
	'''
	condicion : IF OPENPARENTHESIS expression CLOSEPARENTHESIS pn_3 bloque condicionAuxiliar SEMICOLON
	| IF OPENPARENTHESIS expression CLOSEPARENTHESIS pn_3 bloque condicionAuxiliar
	'''
def p_pn_3(p):
	'''
	pn_3 : empty
	'''
	if len(currentProgram.expStack) == 0:
		p.error()
	currentProgram.generateIFJump("gotoF", currentProgram.expStack.pop())
def p_pn_4(p):
	'''
	pn_4 : empty
	'''
	currentProgram.fillIFJump()

def p_condicionAuxiliar(p):
	'''
	condicionAuxiliar : pn_9 ELSE bloque pn_5
	| pn_4 empty
	'''
def p_pn_9(p):
	'''
	pn_9 : empty
	'''
	currentProgram.endTRUEIF()
	currentProgram.fillIFJump()

def p_pn_5(p):
	'''
	pn_5 : empty
	'''
	currentProgram.fillIFJump()

def p_expression(p):
	'''expression : exploc logicexp'''
	p[0] = p[1]
	return p[0]

def p_logicexp(p):
	'''logicexp : OR andor exploc top_andor
	| AND andor exploc top_andor
	| empty'''

def p_exploc(p):
	'''exploc : exp expression1'''
	p[0] = p[1]
	return p[0]

def p_expression1(p):
	'''expression1 : LESSER relop exp top_relop
	| GREATER relop exp top_relop
	| EQUALEQUAL relop exp top_relop
	| NOTEQUAL relop exp top_relop
	| GREATEROREQUAL relop exp top_relop
	| LESSEROREQUAL relop exp top_relop
	| empty'''


def p_exp(p):
	'''exp : term top_exp exp1'''
	p[0] = p[1]
	return p[0]

def p_exp1(p):
	'''exp1 : MINUS push_sign exp
	| PLUS push_sign exp
	| empty'''


def p_top_exp(p):
	'''
	top_exp : empty
	'''
	if len(currentProgram.opStack) > 0:
		operator = currentProgram.opStack[len(currentProgram.opStack) - 1]
		if operator == "+" or operator == "-":
			operator = currentProgram.opStack.pop()
			r_operand = currentProgram.expStack.pop()
			l_operand =  currentProgram.expStack.pop()
			t = currentProgram.getTempMemory()
			currentProgram.cuadruplos.append([operator,l_operand,r_operand, t])
			currentProgram.expStack.append(t)

def p_term(p):
	'''term : factor top_factor term1'''
	return p[1]

def p_term1(p):
	'''term1 : DIVIDE push_sign term
		| TIMES push_sign term
		| empty'''

def p_factor(p):
	'''factor : OPENPARENTHESIS false_bottom expression CLOSEPARENTHESIS end_par
	| var_cte
	| ID push_id
	'''
	if len(p) > 3:
		p[0] = p[3]
	else:
		p[0] = p[1]
	return p[0]

def p_top_factor(p):
	'''top_factor : '''
	if len(currentProgram.opStack) > 0:
		operator = currentProgram.opStack[len(currentProgram.opStack) - 1]
		if operator == "*" or operator == "/":
			#print(currentProgram.expStack)
			operator = currentProgram.opStack.pop()
			r_operand = currentProgram.expStack.pop()
			l_operand =  currentProgram.expStack.pop()
			t  = currentProgram.getTempMemory()
			currentProgram.cuadruplos.append([operator,l_operand,r_operand, t])
			currentProgram.expStack.append(t)


def p_var_cte(p):
	'''var_cte :  arregloVar
				| CTEINT getvalue_i
				| CTEFLOAT getvalue_f
				| ID getidvalue
				| llamada getidllamada
				| spcte
	'''
	if len(p) > 3:
		p[0] = p[3]
	elif len(p) > 2:
		p[0] = p[2]
		return p[0]


def p_getidllamada(p):
	'''getidllamada : empty'''
	#print(currentProgram.opStack)

def p_getarrayvalue(p):
	'''getarrayvalue : '''
	currentProgram.expStack.append(p[-1])


def p_getidvalue(p):
	'''getidvalue : '''
	dir = currentProgram.getVarDir(p[-1])

	currentProgram.expStack.append(dir)
	if  dir == -1:
		print("var not definded: " + p[-1] + " at line " + str(p.lineno(-1)))
		print(-1)
		sys.exit()


def p_getvalue_i(p):
	'''getvalue_i : '''
	t = currentProgram.getConstMemory(p[-1], "int")
	currentProgram.expStack.append(t)


def p_getvalue_f(p):
	'''getvalue_f : '''
	t = currentProgram.getConstMemory(p[-1], "float")
	currentProgram.expStack.append(t)

def p_getvalue_b(p):
	'''getvalue_b : '''
	#currentProgram.expStack.append(p[-1])

def p_relop(p):
	'''relop : '''
	op = p[-1]
	if op == '<':
		currentProgram.opStack.append("<")
	if op == '>':
		currentProgram.opStack.append(">")
	if op == '<=':
		currentProgram.opStack.append("<=")
	if op == '==':
		currentProgram.opStack.append("==")
	if op == '>=':
		currentProgram.opStack.append(">=")
	if op == '!=':
		currentProgram.opStack.append("!=")

def p_andor(p):
	'''andor : '''
	op = p[-1]
	if op == 'and':
		currentProgram.opStack.append("and")
	if op == 'or':
		currentProgram.opStack.append("or")

def p_top_andor(p):
	'''top_andor :'''
	if len(currentProgram.opStack) > 0:
		operator = currentProgram.opStack[len(currentProgram.opStack) - 1]
		if operator == "<" or operator == "or" or operator == "and":
			operator = currentProgram.opStack.pop()
			r_operand = currentProgram.expStack.pop()
			l_operand =  currentProgram.expStack.pop()
			t  = currentProgram.getTempMemory()
			currentProgram.cuadruplos.append([operator,l_operand,r_operand, t])
			currentProgram.expStack.append(t)

def p_top_relop(p):
	'''top_relop :'''
	if len(currentProgram.opStack) > 0:
		operator = currentProgram.opStack[len(currentProgram.opStack) - 1]
		if operator == "<" or operator == ">" or operator == "<=" or operator == "==" or operator == ">=" or operator == "!=":
			operator = currentProgram.opStack.pop()
			r_operand = currentProgram.expStack.pop()
			l_operand =  currentProgram.expStack.pop()
			t  = currentProgram.getTempMemory()
			currentProgram.cuadruplos.append([operator,l_operand,r_operand, t])
			currentProgram.expStack.append(t)

def p_push_sign(p):
	'''push_sign :'''
	if not p[-1] is None:
		sign = p[-1]
	if sign is "/":
		currentProgram.opStack.append("/")
	elif sign is "*":
		currentProgram.opStack.append("*")
	elif sign is "+":
		currentProgram.opStack.append("+")
	elif sign is "-":
		currentProgram.opStack.append("-")
	elif sign is "=":
		currentProgram.opStack.append("=")

def p_false_bottom(p):
	'''false_bottom : empty'''
	currentProgram.opStack.append("(")

def p_end_par(p):
	'''end_par :'''
	#print( currentProgram.opStack)
	if currentProgram.opStack[len(currentProgram.opStack) - 1] is "(":
		currentProgram.opStack.pop()


def p_push_id(p):
	'''push_id : '''
	dir = currentProgram.getVarDir(p[-1])
	if dir == -1:
		print("var not definded: " + p[-1] + " at line " + str(p.lineno(-1)))
		print(-1)
		sys.exit()


def p_ctebool(p):
	'''
	ctebool : TRUE
	| FALSE
	'''
	t = currentProgram.getConstMemory(p[1], "bool")
	currentProgram.expStack.append(t)

def p_spcte(p):
	'''
	spcte : CTESTRING
	| ctebool
	'''
	if p[1] != None:
		t = currentProgram.getConstMemory(p[1], "texto")
		currentProgram.expStack.append(t)


def p_error(p):
	if p is not None:
		print ("Line %s:\nInvalid token -> %s" % (p.lineno, p.value))
		print(-1)
		sys.exit()
	print(-1)
	sys.exit()

lex.lex()
yacc.yacc(start = 'programa')

if __name__ == '__main__':
	if(len(sys.argv) > 1):
		file = sys.argv[1]
		try:
			f = open(file,'r')
			data = f.read()
			f.close()
			if(yacc.parse(data, tracking = True)):
				print("Success")
				i = 0
				pprint(currentProgram)
				for quad in currentProgram.cuadruplos:
					print(i.__str__() + quad.__str__())
					i = i + 1
				data = currentProgram.prepareData()
				print(json.dumps(data))

			else:
				print("Error detected")
				print(-1)
				sys.exit()
		except EOFError:
			print(EOFError)
			print(-1)
			sys.exit()
	else:
		print('Type a file name')
		print(-1)
		sys.exit()
