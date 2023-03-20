import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'INT', 
    'FLOAT',
    'ID', 
    'PLUS', 
    'MINUS', 
    'DIVIDE',
    'MULTIPLY', 
    'EQUALS', 
    'SEMICOLON', 
    'COLON', 
    'LEFTBRACKET', 
    'RIGHTBRACKET', 
    'LEFTPAREN', 
    'RIGHTPAREN', 
    'GREATER', 
    'LESSER', 
    'DIFF', 
    'COMMA', 
    'PROGRAM', 
    'PRINT',
    'IF', 
    'ELSE', 
    'VAR', 
    'CTESTRING',
    'CTEI', 
    'CTEF', 
]

t_SEMICOLON = r'\;'
t_COLON = r':'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_CTESTRING = r'\".*\"'
t_GREATER = r'>'
t_LESSER = r'<'
t_DIFF = r'<>'
t_LEFTBRACKET = r'\{'
t_RIGHTBRACKET = r'\}'
t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
t_COMMA = r'\,'

t_ignore = r' '

keywords = {
    'int': 'INT',
    'float': 'FLOAT',
    'program': 'PROGRAM',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'var': 'VAR',
}

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
def t_ID(t):
    r'[a-zA-z]([a-zA-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_comment(t):
    r'\//.*'
    pass
def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)

lexer = lex.lex()

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None
def p_expression(p):
    '''
    expression : exp comparation
    '''
def p_var_cte(p):
    '''var_cte : ID
    | CTEI
    | CTEF
    '''
def p_program(p):
    '''program : PROGRAM ID SEMICOLON program_vars block'''
    p[0] = "COMPILED"
def p_program_vars(p):
    '''
    program_vars : vars
    | empty
    '''
def p_block(p):
    '''
    block : LEFTBRACKET statement_block RIGHTBRACKET
    '''
def p_statement_block(p):
    '''
    statement_block : statement statement_block
    | empty
    '''
def p_statement(p):
    '''statement : assignment
    | condition
    | writing'''

def p_comparation(p):
    '''
    comparation : GREATER comparation_exp
    | LESSER comparation_exp
    | DIFF comparation_exp
    | empty
    '''
def p_comparation_exp(p):
    '''
    comparation_exp : exp
    '''
def p_exp(p):
    '''
    exp : term operator
    '''
def p_operator(p):
    '''
    operator : PLUS term operator
    | MINUS term operator
    | empty
    '''
def p_term(p):
    '''
    term : factor term_operator
    '''
def p_term_operator(p):
    '''
    term_operator : MULTIPLY factor term_operator
    | DIVIDE factor term_operator
    | empty
    '''
def p_factor(p):
    '''
    factor : LEFTPAREN expression RIGHTPAREN
    | sign var_cte
    '''
def p_sing(p):
    '''
    sign : PLUS
    | MINUS
    | empty
    '''
def p_vars(p):
    '''
    vars : VAR var_id COLON type SEMICOLON vars_block
    '''
def p_var_id(p):
    '''
    var_id : ID var_id_2
    '''
def p_var_id_2(p):
    '''
    var_id_2 : COMMA ID var_id_2
    | empty
    '''
def p_type(p):
    '''
    type : INT
    | FLOAT
    '''
def p_vars_block(p):
    '''
    vars_block : var_id COLON type SEMICOLON vars_block
    | empty
    '''
def p_assignment(p):
    '''
    assignment : ID EQUALS expression SEMICOLON
    '''
def p_condition(p):
    '''
    condition : IF LEFTPAREN expression RIGHTPAREN block else_condition SEMICOLON
    '''
def p_else_condition(p):
    '''
    else_condition : ELSE block
    | empty
    '''
def p_writing(p):
    '''
    writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON
    '''
def p_print_val(p):
    '''
    print_val : expression print_exp
    | CTESTRING print_exp
    '''
def p_print_exp(p):
    '''
    print_exp : COMMA  print_val
    | empty
    '''
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)