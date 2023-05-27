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

#  La funcion para el token NUME que si iplica valor
def t_NUME(t):
    r'[0-9]+\.[0-9]+|[0-9]+'
    t.value = float(t.value)
    return t

# Función para manejar errores lexicos
def t_error(t):
    st.error("Hubo un error lexico...")
    
# La regla (S -> E EOL)
def p_s(p):
    '''s : e EOL'''
    p[0] = p[1]
    print(p[0])

## La funcion para las reglas (E -> E + T y E -> E - T)
## Calcula cuando hay una suma o resta
def p_e1(p):
    '''e : e SUMA t
         | e RESTA t'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

## La funcion que implementa la regla (E -> T)
def p_e2(p):
    '''e : t'''
    p[0] = p[1]

## La funcion para las reglas (T -> T * F y T -> T / F)
## Calcula cuando hay una multiplicacion o divicion
def p_t1(p):
    '''
    t : t MULT f
      | t DIV f
    '''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1] / p[3]

## Esta función implementa (T -> F)
def p_t2(p):
    '''t : f'''
    p[0] = p[1]

## Funcion que implementa F -> ( E )
## Calcula cuando se abre un parentesis izquierdo y se cierra con uno derecho
def p_f1(p):
    '''f : PARIZQ e PARDER'''
    p[0] = p[2]

## Esta función implementa F -> nunme
def p_f2(p):
    '''f : NUME'''
    p[0] = p[1]

## Para manejar errores sintacticos
def p_error(p):
    if p:
        st.error("Error de sintaxis en el símbolo:", p.value)
    else:
        st.error("Error de sintaxis en la entrada")

# Definicion de variables del lexer y parser
lexer = lex.lex()
parser = yacc.yacc()

# Captura de la expresion del usuario
entrada = st.text_input("Expresión ") + '\n'

# Boton para calcular el resultado de la expresion si es correcta la expresion
if st.button("Calcular"):
    if parser.parse(entrada, lexer=lexer):
        st.success(f'{entrada} = {parser.parse(entrada, lexer=lexer):.3f}')
    else:
        st.error("La expresión no es válida")