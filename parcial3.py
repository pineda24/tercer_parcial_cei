import ply.lex as lex
import ply.yacc as yacc
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Parcial 3 - COMPILADORES E INTERPRESES"
)

# Título y detalles del equipo
st.title("Parcial 3 - COMPILADORES E INTERPRESES")
st.write("338710 - MARIO ALBERTO TERAN ACOSTA")
st.write("338919 - RAUL HIRAM PINEDA CHAVEZ")


# Definición de tokens
tokens = ('NUME', 'SUMA', 'RESTA', 'MULT', 'DIV', 'PARIZQ', 'PARDER', 'EOL')

# Expresiones regulares para los tokens
t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_EOL = r'\n'

# Función para tokenizar números
def t_NUME(t):
    r'[0-9]+\.[0-9]+|[0-9]+'
    t.value = float(t.value)
    return t

# Función de error para manejar caracteres no reconocidos
def t_error(t):
    st.error("Hubo un error lexico...")
    
# Definición de la regla inicial de la gramática
def p_s(p):
    '''s : e EOL'''
    p[0] = p[1]
    print(p[0])

# Reglas de la gramática para la expresión aritmética
def p_e1(p):
    '''e : e SUMA t
         | e RESTA t'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

def p_e2(p):
    '''e : t'''
    p[0] = p[1]

def p_t1(p):
    '''
    t : t MULT f
      | t DIV f
    '''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1] / p[3]

def p_t2(p):
    '''t : f'''
    p[0] = p[1]

def p_f1(p):
    '''f : PARIZQ e PARDER'''
    p[0] = p[2]

def p_f2(p):
    '''f : NUME'''
    p[0] = p[1]

def p_error(p):
    if p:
        print("Error de sintaxis en el símbolo:", p.value)
    else:
        print("Error de sintaxis en la entrada")

# Construcción del lexer y parser
lexer = lex.lex()
parser = yacc.yacc()

# Captura de la entrada del usuario
entrada = st.text_input("Expresión ")
entrada += '\n'

# Análisis de la expresión y cálculo del resultado
if st.button("Calcular"):
    if parser.parse(entrada, lexer=lexer):
        st.success(f'{entrada} = {parser.parse(entrada, lexer=lexer):.3f}')
    else:
        st.error("La expresión no es válida")