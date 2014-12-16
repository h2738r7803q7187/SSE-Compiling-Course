# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'H1','H2','H3', 'CR', 'TEXT'
    )

# Tokens
t_H1 = r'\# '
t_H2 = r'\#\# '
t_H3 = r'\#\#\# '

def t_TEXT(t):
    r'[_a-zA-Z0-9]+'
    t.value = str(t.value)
    return t

t_ignore = " \t"

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()


precedence = (
    )

names = { }

def p_body(p):
    '''body : statement'''
    print '<body>' + p[1] + '</body>'

def p_state(p):
    '''statement : expression
            | statement CR expression'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + '<br>' + str(p[3])

def p_exp_cr(p):
    '''expression : H1 factor
                | H2 factor
                | H3 factor'''
    p[0] = '<h1>' + str(p[2]) + '</h1>'

def p_factor_text(p):
    "factor : TEXT"
    p[0] = p[1]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    filename = 'test.md'
    yacc.parse(open(filename).read())
