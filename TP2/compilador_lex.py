import ply.lex as lex
import sys

tokens = ['ID','INT','FLOAT','INT_A','FLOAT_A','STRING_A','EQUAL','STRING','FOR','READ',
            'AND','OR','LESS_EQUAL','MORE_EQUAL','EQUAL_EQUAL','DIF','PRINT','IF','ELSE']
literals = ['+','-','*','/','%','(',')',';','{','}','[',']','>','<','!']

def t_READ(t):
    r'read\ *'
    t.value = str(t.value)
    return t

def t_FOR(t):
    r'for\ *'
    t.value = str(t.value)
    return t

def t_IF(t):
    r'if\ *'
    t.value = str(t.value)
    return t

def t_ELSE(t):
    r'else\ *'
    t.value = str(t.value)
    return t

def t_AND(t):
    r'&&'
    t.value = str(t.value)
    return t

def t_OR(t):
    r'\|\|'
    t.value = str(t.value)
    return t

def t_LESS_EQUAL(t):
    r'\<\='
    t.value = str(t.value)
    return t

def t_MORE_EQUAL(t):
    r'\>\='
    t.value = str(t.value)
    return t

def t_EQUAL_EQUAL(t):
    r'\=\='
    t.value = str(t.value)
    return t

def t_DIF(t):
    r'\!\='
    t.value = str(t.value)
    return t

def t_PRINT(t):
    r'print\ +'
    t.value = str(t.value)
    return t

def t_INT_A(t):
    r'int\ +'
    t.value = str(t.value)
    return t

def t_FLOAT_A(t):
    r'float\ +'
    t.value = str(t.value)
    return t

def t_STRING_A(t):
    r'string\ +'
    t.value = str(t.value)
    return t

def t_EQUAL(t):
    r'=\ *'
    t.value = str(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
def t_ID(t):
    r'\w+\ *'
    t.value = str(t.value)
    return t

def t_STRING(t):
    r'\"[^"]+\"'
    t.value = str(t.value)
    return t    

def t_error(t):
    print('Illegal character: '+t.value[0])
    t.lexer.skip(1)


t_ignore = ' \n\t'

lexer = lex.lex()

""" for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:
        print(tok) """