import ply.lex as lex
import sys

tokens = ['ID','INT','FLOAT','INT_A','FLOAT_A','STRING_A','EQUAL','STRING',
            'AND','OR','LESS_EQUAL','MORE_EQUAL','EQUAL_EQUAL','PRINT']
literals = ['+','-','*','/','(',')',';','{','}','[',']','>','<','!']

t_AND = r'&&'
t_OR = r'\|\|'
t_LESS_EQUAL = r'\<\='
t_MORE_EQUAL = r'\>\='
t_EQUAL_EQUAL = r'\=\='
t_PRINT = r'print\ +'
t_INT_A = r'int\ +'
t_FLOAT_A = r'float\ +'
t_STRING_A = r'string\ +'
t_ID = r'\w+\ *'
t_EQUAL = r'=\ *'
t_STRING = r'\"[^"]+\"'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
    

def t_error(t):
    print('Illegal character: '+t.value[0])
    t.lexer.skip(1)


t_ignore = ' \n\t'

lexer = lex.lex()
