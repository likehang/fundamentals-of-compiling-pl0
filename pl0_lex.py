#pl0 2018-1-7  15:59

from ply.lex import lex
import sys

# '+' not find ! 2018-1-8 11:20 
reserved = {
    'begin':'BEGIN',
    'call':'CALL',
    'if':'IF',
    'for':'FOR',
    'read':'READ',
    'while':'WHILE',
    'write':'WRITE',
    }
block = {
    'array':'ARRAY',
    'const':'CONST',
    'procedure':'PROCEDURE',
    'var':'VAR',
    }
recent = {
    'do':'DO',
    'then':'THEN',
    'end':'END',
    'else':'ELSE',
    'repeat':'REPEAT',
    }
tokens = ['ID','LZPAREN','RZPAREN','DPLUS','DMINUS',
          'LPAREN','RPAREN','NUMBER','PLUS','MINUS','TIMES','SLASH','COM',
          'EQEQ','GE','LE', 'GT','LT','EQ','NEQ','CEQ','DOT','COMMA','EOS','ODD',
          
          ]+list(reserved.values())+list(block.values())+list(recent.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if (t.value in reserved) or (t.value in block) or (t.value in recent) :
        t.value = t.value.upper()
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+|(\r\n)+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    #print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_COMMENT_ignore(t):
    r'\\\\.*' 
    pass
t_ignore = r' '
t_ODD = r'odd'
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_SLASH  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQEQ = r'=='
t_EQ = r':='
t_CEQ = r'='
t_NEQ =r'\#'
t_COMMA =r','
t_EOS =r';'
t_COM = r'!'
t_DOT = r'\.'
t_LZPAREN = r'\['
t_RZPAREN = r'\]'
t_DPLUS = r'\+\+'
t_DMINUS = r'--'

def create():
    return lexer.clone()

lexer=lex()

if __name__ =='__main__':
    filename = input('please input the filename : ')
    tokenfile = open('pl0_token.txt','wt')
    f = open(filename).read()
    lexer.input(f)
    while True:
        gettok = lexer.token()
        if not gettok:
            break;
        print(gettok)
        print(gettok,file = tokenfile)
