import ply.yacc as yacc
import sys

output = open("output.vm","w+")

from compilador_lex import tokens

def p_body(p):
    "body : '(' atribuicoes operacoes"
    p[0] = p[2] + "START\n" + p[3]
    
def p_atribuicoes_atribuicao(p):
    "atribuicoes : atribuicoes atribuicao"
    p[0] = p[1]+p[2]

def p_atribuicoes_vazio(p):
    "atribuicoes : "
    p[0] = ""

def p_atribuicao_int(p):
    "atribuicao : INT_A ID EQUAL INT ';'"
    p.parser.variaveis_int[p[2].strip()] = p.parser.variaveis
    p.parser.variaveis += 1
    p[0] = f"pushi {p[4]}\n"

def p_atribuicao_float(p):
    "atribuicao : FLOAT_A ID EQUAL FLOAT ';'"
    p.parser.variaveis_float[p[2].strip()] = p.parser.variaveis
    p.parser.variaveis += 1
    p[0] = f"pushf {p[4]}\n"

def p_atribuicao_int_null(p):
    "atribuicao : INT_A ID ';'"
    p.parser.variaveis_int[p[2].strip()] = p.parser.variaveis
    p.parser.variaveis += 1
    p[0] = "pushi 0\n"

def p_atribuicao_float_null(p):
    "atribuicao : FLOAT_A ID ';'"
    p.parser.variaveis_float[p[2].strip()] = p.parser.variaveis
    p.parser.variaveis += 1
    p[0] = "pushf 0.0\n"

def p_atribuicao_array(p):
    "atribuicao : INT_A ID '[' INT ']' ';'"
    p.parser.variaveis_arrays[p[2].strip()] = (p.parser.variaveis,p.parser.variaveis+p[4]-1)
    p.parser.variaveis += p[4]
    p[0] = f"pushn {p[4]}\n"

def p_atribuicao_array2d(p):
    "atribuicao : INT_A ID '[' INT ']' '[' INT ']' ';'"
    p.parser.variaveis_arrays2d[p[2].strip()] = (p.parser.variaveis,p.parser.variaveis+(p[4]*p[7])-1,p[7])
    p.parser.variaveis += p[4]*p[7]
    p[0] = f"pushn {p[4]*p[7]}\n"


def p_atribuicao_string(p):
    "atribuicao : STRING_A ID EQUAL STRING ';'"
    p.parser.variaveis_string[p[2].strip()] = p.parser.variaveis
    p.parser.variaveis += 1
    p[0] = f"pushs {p[4]}\n"


def p_operacoes_operacao(p):
    "operacoes : operacoes operacao "
    p[0] = p[1] + p[2]

def p_operacoes_fim(p):
    "operacoes : "
    p[0] = ""

#TODO verificar que n está outofbounds e que de facto é um array
def p_operacao_array_valor(p):
    "operacao : ID '[' INT ']' EQUAL expressao ';' "
    aux  = "pushgp\n"
    aux += f"pushi {p.parser.variaveis_arrays[p[1]][0]}\n"
    aux += "padd\n"
    aux += f"pushi {p[3]}\n"
    aux += f"{p[6]}\n"
    aux += "storen\n"
    p[0] = aux

#TODO verificar que n está outofbounds e que de facto é um array
def p_operacao_array2d_valor(p):
    "operacao : ID '[' INT ']' '[' INT ']' EQUAL expressao ';' "
    aux  = "pushgp\n"
    aux += f"pushi {p.parser.variaveis_arrays2d[p[1]][0]}\n"
    aux += "padd\n"
    aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1]][2]+p[6]}\n"
    aux += f"{p[9]}\n"
    aux += "storen\n"
    p[0] = aux

def p_expressao_mais(p):
    "expressao : expressao '+' termo"
    p[0] = p[0] = f"{p[1]}\n{p[3]}\nadd\n"

def p_expressao_menos(p):
    "expressao : expressao '-' termo"
    p[0] = p[0] = f"{p[1]}\n{p[3]}\nsub\n"

def p_expressao_termo(p):
    "expressao : termo"
    p[0] = p[1]

def p_termo_mult(p):
    "termo : termo '*' fator"
    p[0] = f"{p[1]}\n{p[3]}\nmul\n"

def p_termo_div(p):
    "termo : termo '/' fator"
    p[0] = f"{p[1]}\n{p[3]}\ndiv\n"

def p_termo_fator(p):
    "termo : fator"
    p[0] = p[1]

#quanto mais abaixo def mais prioridade
def p_fator_NUM(p):
    "fator : INT "
    p[0] = f"pushi {p[1]}"

def p_fator_expressao(p):
    "fator : '(' expressao ')' "
    p[0] = p[2]

def p_fator_int(p):
    "fator : ID"
    if p[1] in p.parser.variaveis_int:
        p[0] = f"pushg {p.parser.variaveis_int[p[1]]}"
    elif p[1] in p.parser.variaveis_float:
        p[0] = f"pushg {p.parser.variaveis_float[p[1]]}"

#TODO outofbounds
def p_fator_array(p):
    "fator : ID '[' INT ']' "
    aux  = "pushgp\n"
    aux += f"pushi {p.parser.variaveis_arrays[p[1]][0]}\n"
    aux += "padd\n"
    aux += f"pushi {p[3]}\n"
    aux += "loadn\n"
    p[0] = aux

def p_fator_array2d(p):
    "fator : ID '[' INT ']' '[' INT ']' "
    aux  = "pushgp\n"
    aux += f"pushi {p.parser.variaveis_arrays2d[p[1]][0]}\n"
    aux += "padd\n"
    aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1]][2]+p[6]}\n"
    aux += "loadn\n"
    p[0] = aux

    














def p_error(p):
    print("Syntax error! ",p)
    parser.success = False

def atribui_int(valor):
    output.write(f"pushi {valor}\n")

def atribui_float(valor):
    output.write(f"pushf {valor}\n")

parser = yacc.yacc()
parser.variaveis_int = {}
parser.variaveis_float = {}
parser.variaveis_arrays = {}
parser.variaveis_arrays2d = {}
parser.variaveis_string = {}
parser.variaveis = 0
result = ""


with open(sys.argv[1],"r") as f:
    parser.success = True
    result += parser.parse(f.read())

if parser.success:
    print(f"//{parser.variaveis_int}")
    print(f"//{parser.variaveis_float}")
    print(f"//{parser.variaveis_arrays}")
    print(f"//{parser.variaveis_arrays2d}")
    print(f"//{parser.variaveis_string}")
    print(result)
    
