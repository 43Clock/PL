import sys

import ply.yacc as yacc
import re

output = open("output.vm","w+")

from compilador_lex import tokens


def p_body(p):
    "body : atribuicoes operacoes"
    p[0] = p[1] + "START\n" + p[2] + "STOP\n"
    
def p_atribuicoes_atribuicao(p):
    "atribuicoes : atribuicoes atribuicao"
    p[0] = p[1]+p[2]

def p_atribuicoes_vazio(p):
    "atribuicoes : "
    p[0] = ""

def p_atribuicao_int(p):
    "atribuicao : INT_A ID EQUAL INT ';'"
    if not p[2].strip() in p.parser.variaveis_int and not p[2].strip() in p.parser.variaveis_arrays and not p[2].strip() in p.parser.variaveis_arrays2d and not p[2].strip() in p.parser.variaveis_string:
        p.parser.variaveis_int[p[2].strip()] = p.parser.variaveis
        p.parser.variaveis += 1
        p[0] = f"pushi {p[4]}\n"
    else:
        p.parser.success = False
        p.parser.erro = f"Variável '{p[2]}' já definida\n"
        p[0] = ""

def p_atribuicao_int_null(p):
    "atribuicao : INT_A ID ';'"
    if not p[2].strip() in p.parser.variaveis_int and not p[2].strip() in p.parser.variaveis_arrays and not p[2].strip() in p.parser.variaveis_arrays2d and not p[2].strip() in p.parser.variaveis_string:
        p.parser.variaveis_int[p[2].strip()] = p.parser.variaveis
        p.parser.variaveis += 1
        p[0] = "pushi 0\n"
    else:
        p.parser.success = False
        p.parser.erro = f"Variável '{p[2]}' já definida\n"
        p[0] = ""
  

def p_atribuicao_array(p):
    "atribuicao : INT_A ID '[' INT ']' ';'"
    if not p[2].strip() in p.parser.variaveis_int and not p[2].strip() in p.parser.variaveis_arrays and not p[2].strip() in p.parser.variaveis_arrays2d and not p[2].strip() in p.parser.variaveis_string:
        p.parser.variaveis_arrays[p[2].strip()] = (p.parser.variaveis,p.parser.variaveis+p[4]-1)
        p.parser.variaveis += p[4]
        p[0] = f"pushn {p[4]}\n"
    else:
        p.parser.success = False
        p.parser.erro = f"Variável '{p[2]}' já definida\n"
        p[0] = ""     

def p_atribuicao_array2d(p):
    "atribuicao : INT_A ID '[' INT ']' '[' INT ']' ';'"
    if not p[2].strip() in p.parser.variaveis_int and not p[2].strip() in p.parser.variaveis_arrays and not p[2].strip() in p.parser.variaveis_arrays2d and not p[2].strip() in p.parser.variaveis_string:
        p.parser.variaveis_arrays2d[p[2].strip()] = (p.parser.variaveis,p.parser.variaveis+(p[4]*p[7])-1,p[7])
        p.parser.variaveis += p[4]*p[7]
        p[0] = f"pushn {p[4]*p[7]}\n"
    else:
        p.parser.success = False
        p.parser.erro = f"Variável '{p[2]}' já definida\n"
        p[0] = ""
        
def p_atribuicao_string(p):
    "atribuicao : STRING_A ID EQUAL STRING ';'"
    if not p[2].strip() in p.parser.variaveis_int and not p[2].strip() in p.parser.variaveis_arrays and not p[2].strip() in p.parser.variaveis_arrays2d and not p[2].strip() in p.parser.variaveis_string:
        p.parser.variaveis_string[p[2].strip()] = p.parser.variaveis
        p.parser.variaveis += 1
        p[0] = f"pushs {p[4]}\n"
    else:
        p.parser.success = False
        p.parser.erro = f"Variável '{p[2]}' já definida\n"
        p[0] = ""

def p_operacoes_operacao(p):
    "operacoes : operacoes operacao"
    p[0] = p[1] + p[2] 
    
def p_operacoes_operacao_inc(p):
    "operacoes : operacoes operacao_inc"
    if p.parser.success:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""   

def p_operacoes_fim(p):
    "operacoes : "
    p[0] = ""

def p_operacao_inc_variavel_incrementar(p):
    "operacao_inc : ID '+' '+' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            aux = f"pushg {p.parser.variaveis_int[p[1].strip()]}\n"
            aux += f"pushi 1\n"
            aux += f"add\n"
            aux += f"storeg {p.parser.variaveis_int[p[1].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""   
    else:
        p[0] = ""   

def p_operacao_inc_variavel_decrementar(p):
    "operacao_inc : ID '-' '-' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            aux = f"pushg {p.parser.variaveis_int[p[1].strip()]}\n"
            aux += f"pushi 1\n"
            aux += f"sub\n"
            aux += f"storeg {p.parser.variaveis_int[p[1].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""  
    else:
        p[0] = ""

def p_operacao_inc_variavel_plus_equal(p):
    "operacao_inc : ID '+' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            aux = f"pushg {p.parser.variaveis_int[p[1].strip()]}\n"
            aux += f"{p[4]}\n"
            aux += f"add\n"
            aux += f"storeg {p.parser.variaveis_int[p[1].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""   
    else:
        p[0] = ""    

def p_operacao_inc_variavel_minus_equal(p):
    "operacao_inc : ID '-' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            aux = f"pushg {p.parser.variaveis_int[p[1].strip()]}\n"
            aux += f"{p[4]}\n"
            aux += f"sub\n"
            aux += f"storeg {p.parser.variaveis_int[p[1].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n" 
            p[0] = ""  
    else:
        p[0] = ""      
   

def p_operacao_inc_array_incrementar(p):
    "operacao_inc : ID '[' INT ']' '+' '+' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += f"pushg {p.parser.variaveis_arrays[p[1].strip()][0]+p[3]}\n"
            aux += f"pushi 1\n" 
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""   

def p_operacao_inc_array_incrementar_id(p):
    "operacao_inc : ID '[' ID ']' '+' '+' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n" #Fazer isto again para ir buscar o valor na posicao ID
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "loadn\n"
            aux += f"pushi 1\n" 
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""    

def p_operacao_inc_array_decrementar(p):
    "operacao_inc : ID '[' INT ']' '-' '-' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += f"pushg {p.parser.variaveis_arrays[p[1].strip()][0]+p[3]}\n"
            aux += f"pushi 1\n" 
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""       

def p_operacao_inc_array_decrementar_id(p):
    "operacao_inc : ID '[' ID ']' '-' '-' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n" #Fazer isto again para ir buscar o valor na posicao ID
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "loadn\n"
            aux += f"pushi 1\n" 
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      

def p_operacao_inc_array_plus_equal(p):
    "operacao_inc : ID '[' INT ']' '+' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += f"pushg {p.parser.variaveis_arrays[p[1].strip()][0]+p[3]}\n"
            aux += f"{p[7]}\n"
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""       

def p_operacao_inc_array_plus_equal_id(p):
    "operacao_inc : ID '[' ID ']' '+' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n" #Fazer isto again para ir buscar o valor na posicao ID
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "loadn\n"
            aux += f"{p[7]}\n"
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      

def p_operacao_inc_array_minus_equal(p):
    "operacao_inc : ID '[' INT ']' '-' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += f"pushg {p.parser.variaveis_arrays[p[1].strip()][0]+p[3]}\n"
            aux += f"{p[7]}\n"
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      

def p_operacao_inc_array_minus_equal_id(p):
    "operacao_inc : ID '[' ID ']' '-' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n" #Fazer isto again para ir buscar o valor na posicao ID
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "loadn\n"
            aux += f"{p[7]}\n"
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""     

def p_operacao_inc_array2d_incrementar(p):
    "operacao_inc : ID '[' INT ']' '[' INT ']' '+' '+' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushg {p.parser.variaveis_arrays2d[p[1].strip()][0]+p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushi 1\n" 
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""     

def p_operacao_inc_array2d_decrementar(p):
    "operacao_inc : ID '[' INT ']' '[' INT ']' '-' '-' ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushg {p.parser.variaveis_arrays2d[p[1].strip()][0]+p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushi 1\n" 
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      

def p_operacao_inc_array2d_plus_equal(p):
    "operacao_inc : ID '[' INT ']' '[' INT ']' '+' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushg {p.parser.variaveis_arrays2d[p[1].strip()][0]+p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"{p[10]}\n"
            aux += f"add\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      

def p_operacao_inc_array2d_minus_equal(p):  
    "operacao_inc : ID '[' INT ']' '[' INT ']' '-' EQUAL expressao ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"pushg {p.parser.variaveis_arrays2d[p[1].strip()][0]+p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"{p[10]}\n"
            aux += f"sub\n"
            aux += f"storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""      


def p_operacao_variavel(p):
    "operacao : ID EQUAL expressoes ';'"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            aux = f"{p[3]}\n"
            aux += f"storeg {p.parser.variaveis_int[p[1].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n" 
            p[0] = ""  
    else:
        p[0] = ""   

def p_operacao_array2d_valor(p):
    "operacao : ID '[' INT ']' '[' INT ']' EQUAL expressoes ';' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += f"{p[9]}\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""   

def p_operacao_array_valor(p):
    "operacao : ID '[' INT ']' EQUAL expressoes ';' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += f"{p[6]}\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""        


def p_operacao_array_valor_id(p):
    "operacao : ID '[' ID ']' EQUAL expressoes ';' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += f"{p[6]}\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = "" 
    else:
        p[0] = ""     

def p_imprime_var(p):
    "operacao : PRINT ID ';' "
    if p.parser.success:
        aux = ""
        if p[2].strip() in p.parser.variaveis_int:
            aux += f"pushg {p.parser.variaveis_int[p[2].strip()]}\n"
            aux += f"writei\n"
            aux += "pushs \"\\n\"\n"
            aux += "writes\n"    
            p[0] = aux
        elif p[2].strip() in p.parser.variaveis_string:
            aux += f"pushg {p.parser.variaveis_string[p[2].strip()]}\n"
            aux += f"writes\n"
            aux += "pushs \"\\n\"\n"
            aux += "writes\n"    
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""     


def p_imprime_array(p):
    "operacao : PRINT ID '[' INT ']' ';' "
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays:
            if p[4] > p.parser.variaveis_arrays[p[2].strip()][1]-p.parser.variaveis_arrays[p[2].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[4]}\n"
            aux += "loadn\nwritei\n"
            aux += "pushs \"\\n\"\n"
            aux += "writes\n" 
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_imprime_array_id(p):
    "operacao : PRINT ID '[' ID ']' ';' "
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays and p[4].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[4].strip()]}\n"
            aux += "loadn\nwritei\n"
            aux += "pushs \"\\n\"\n"
            aux += "writes\n" 
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' ou '{p[4].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_imprime_array2d(p):
    "operacao : PRINT ID '[' INT ']' '[' INT ']' ';' "
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays2d:
            if p[7] > p.parser.variaveis_arrays2d[p[2].strip()][2]-1 or p[4]>(p.parser.variaveis_arrays2d[p[2].strip()][1]-p.parser.variaveis_arrays2d[p[2].strip()][0])/p.parser.variaveis_arrays2d[p[2].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[4]*p.parser.variaveis_arrays2d[p[2].strip()][2]+p[7]}\n"
            aux += "loadn\nwritei\n"
            aux += "pushs \"\\n\"\n"
            aux += "writes\n" 
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_imprime_string(p):
    "operacao : PRINT STRING ';' "
    p[0] = f"pushs {p[2]}\nwrites\npushs \"\\n\"\nwrites\n"


def p_operacao_if(p):
    "operacao : IF '(' expressao_logica ')' '{' operacoes '}' "
    aux = p[3]
    aux += f"jz fimIf{p.parser.if_count}\n"
    aux += p[6]
    aux += f"fimIf{p.parser.if_count}:\n"
    p.parser.if_count += 1
    p[0] = aux


def p_operacao_if_else(p):
    "operacao : IF '(' expressao_logica ')' '{' operacoes '}' ELSE '{' operacoes '}' "
    aux = p[3]
    aux += f"jz elseIf{p.parser.if_count}\n"
    aux += p[6]
    aux += f"jump fimIf{p.parser.if_count}\n"
    aux += f"elseIf{p.parser.if_count}:\n"
    aux += p[10]
    aux += f"fimIf{p.parser.if_count}:\n"
    p.parser.if_count += 1
    p[0] = aux

def p_operacao_for(p):
    "operacao : FOR '(' ID EQUAL expressao  ';'  expressao_logica   ';' operacao_inc ')' '{' operacoes '}' "
    if p.parser.success:
        if p[3].strip() in parser.variaveis_int:
            aux = p[5]
            aux += f"storeg {parser.variaveis_int[p[3].strip()]}\n"
            aux += f"cicloFor{p.parser.for_count}:\n"
            aux += p[7]
            aux += f"jz cicloForEnd{p.parser.for_count}\n"
            aux += p[12]
            aux += p[9]
            aux += f"jump cicloFor{p.parser.for_count}\n"       
            aux += f"cicloForEnd{p.parser.for_count}:\n"
            p.parser.for_count+=1
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[3].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""   

def p_operacao_read_variavel(p):
    "operacao : READ ID ';' "
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_int:
            aux = ""
            aux += "read\n"
            aux += "atoi\n"
            aux += f"storeg {p.parser.variaveis_int[p[2].strip()]}\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""  
        

def p_operacao_read_array(p):
    "operacao : READ ID '[' INT ']' ';'"
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays:
            if p[4] > p.parser.variaveis_arrays[p[2].strip()][1]-p.parser.variaveis_arrays[p[2].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux = ""
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[4]}\n"
            aux += f"read\n"
            aux += f"atoi\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_operacao_read_array_id(p):
    "operacao : READ ID '[' ID ']' ';'"
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays and p[4].strip() in p.parser.variaveis_int:
            aux = ""
            aux += "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[4].strip()]}\n"
            aux += f"read\n"
            aux += f"atoi\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' ou '{p[4].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_operacao_read_array2d(p):
    "operacao : READ ID '[' INT ']' '[' INT ']' ';' "
    if p.parser.success:
        if p[2].strip() in p.parser.variaveis_arrays2d:
            if p[7] > p.parser.variaveis_arrays2d[p[2].strip()][2]-1 or p[4]>(p.parser.variaveis_arrays2d[p[2].strip()][1]-p.parser.variaveis_arrays2d[p[2].strip()][0])/p.parser.variaveis_arrays2d[p[2].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[2].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[4]*p.parser.variaveis_arrays2d[p[2].strip()][2]+p[7]}\n"
            aux += f"read\n"
            aux += f"atoi\n"
            aux += "storen\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[2].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_expressoes_expressao(p):
    "expressoes : expressao"
    p[0] = p[1]

def p_expressoes_expressao_logica(p):
    "expressoes : expressao_logica" 
    p[0] = p[1]

def p_expressao_mais(p):
    "expressao : expressao '+' termo"
    p[0] = f"{p[1]}{p[3]}add\n"

def p_expressao_menos(p):
    "expressao : expressao '-' termo"
    p[0]  = f"{p[1]}{p[3]}sub\n"

def p_expressao_termo(p):
    "expressao : termo"
    p[0] = p[1]

def p_termo_mult(p):
    "termo : termo '*' fator"
    p[0] = f"{p[1]}{p[3]}mul\n"

def p_termo_div(p):
    "termo : termo '/' fator"
    p[0] = f"{p[1]}{p[3]}div\n"

def p_termo_mod(p):
    "termo : termo '%' fator"
    p[0] = f"{p[1]}{p[3]}mod\n"

def p_termo_fator(p):
    "termo : fator"
    p[0] = p[1]

#quanto mais abaixo def mais prioridade
def p_fator_NUM(p):
    "fator : INT "
    p[0] = f"pushi {p[1]}\n"

def p_fator_expressao(p):
    "fator : '(' expressao ')' "
    p[0] = p[2]

def p_fator_int(p):
    "fator : ID"
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_int:
            p[0] = f"pushg {p.parser.variaveis_int[p[1].strip()]}\n"
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""


def p_fator_array(p):
    "fator : ID '[' INT ']' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays:
            if p[3] > p.parser.variaveis_arrays[p[1].strip()][1]-p.parser.variaveis_arrays[p[1].strip()][0]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]}\n"
            aux += "loadn\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""       

def p_fator_array_id(p):
    "fator : ID '[' ID ']' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays and p[3].strip() in p.parser.variaveis_int:
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushg {p.parser.variaveis_int[p[3].strip()]}\n"
            aux += "loadn\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' ou '{p[3].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""      

def p_fator_array2d(p):
    "fator : ID '[' INT ']' '[' INT ']' "
    if p.parser.success:
        if p[1].strip() in p.parser.variaveis_arrays2d:
            if p[6] > p.parser.variaveis_arrays2d[p[1].strip()][2]-1 or p[3]>(p.parser.variaveis_arrays2d[p[1].strip()][1]-p.parser.variaveis_arrays2d[p[1].strip()][0])/p.parser.variaveis_arrays2d[p[1].strip()][2]:
                p.parser.success = False
                p.parser.erro = f"Array Index Out Of Bounds\n"
            aux  = "pushgp\n"
            aux += f"pushi {p.parser.variaveis_arrays2d[p[1].strip()][0]}\n"
            aux += "padd\n"
            aux += f"pushi {p[3]*p.parser.variaveis_arrays2d[p[1].strip()][2]+p[6]}\n"
            aux += "loadn\n"
            p[0] = aux
        else:
            p.parser.success = False
            p.parser.erro = f"Variável '{p[1].strip()}' não definida\n"
            p[0] = ""
    else:
        p[0] = ""

def p_expressao_relacional_expressao_sup(p):
    "expressao_relacional : expressao '>' expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "sup\n"
    p[0] = aux

def p_expressao_relacional_expressao_inf(p):
    "expressao_relacional : expressao '<' expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "inf\n"
    p[0] = aux

def p_expressao_relacional_expressao_inf_eq(p):
    "expressao_relacional : expressao LESS_EQUAL expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "infeq\n"
    p[0] = aux

def p_expressao_relacional_expressao_sup_eq(p):
    "expressao_relacional : expressao MORE_EQUAL expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "supeq\n"
    p[0] = aux

def p_expressao_relacional_expressao_eq(p):
    "expressao_relacional : expressao EQUAL_EQUAL expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "equal\n"
    p[0] = aux

def p_expressao_relacional_expressao_dif(p):
    "expressao_relacional : expressao DIF expressao"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "equal\n"
    aux += "not\n"
    p[0] = aux

def p_expressao_logica_not(p):
    "expressao_logica : '!' fator_logico"
    aux = f"{p[2]}\n"
    aux += "not\n"
    p[0] = aux

def p_expressao_logica_and(p):
    "expressao_logica : expressao_logica AND fator_logico"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "mul\n"
    p[0] = aux
 
def p_expressao_logica_or(p):
    "expressao_logica : expressao_logica OR fator_logico"
    aux = f"{p[1]}\n"
    aux += f"{p[3]}\n"
    aux += "add\n"
    aux += "pushi 0\n"
    aux += "sup\n"
    p[0] = aux
    
def p_expressao_logica_relacional(p):
    "expressao_logica : fator_logico"
    p[0] = p[1]


def p_fator_logico_expressao_logica(p):
    "fator_logico : '(' expressao_logica ')' "
    p[0] = p[2]

def p_fator_logico_expressao_relacional(p):
    "fator_logico : expressao_relacional "
    p[0] = p[1]


    


def p_error(p):
    print("Syntax error! ",p)
    parser.success = False

def atribui_int(valor):
    output.write(f"pushi {valor}\n")

def atribui_float(valor):
    output.write(f"pushf {valor}\n")

parser = yacc.yacc()
parser.variaveis_int = {}
parser.variaveis_arrays = {}
parser.variaveis_arrays2d = {}
parser.variaveis_string = {}
parser.variaveis = 0
parser.if_count = 1
parser.for_count = 1
parser.erro = ""

with open(sys.argv[1],"r") as f:
    parser.success = True
    result = parser.parse(f.read())

if parser.success:
    s = re.split(r"\.",sys.argv[1])
    if s:
        with open(f"{s[0]}.vm","w+") as f:
            f.write(result)
    else:
        with open(f"{sys.argv[1]}.vm","w+") as f:
            f.write(result)

else:
    print(parser.erro)
