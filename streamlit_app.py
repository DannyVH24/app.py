import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SimplePy IDE", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stTextArea textarea {
        font-family: 'Fira Code', monospace;
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
    }
    div.stButton > button:first-child {
        background-color: #238636;
        color: white;
        border: none;
        font-weight: bold;
    }
    .code-line { font-family: 'Fira Code', monospace; display: block; padding: 2px 10px; white-space: pre-wrap; }
    .line-error { background-color: rgba(248, 81, 73, 0.15); border-left: 4px solid #f85149; color: #ff7b72; }
    .line-number { color: #8b949e; margin-right: 15px; display: inline-block; width: 30px; text-align: right; }
    .scroll-history { max-height: 200px; overflow-y: auto; background-color: #0d1117; padding: 10px; border: 1px solid #30363d; font-family: monospace; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0
if 'codigo_master' not in st.session_state: st.session_state.codigo_master = ""

# --- TOKENS ORIGINALES (ESTRICTOS) ---
reservadas = {
    "entero": "T_TIPO_ENTERO", "decimal": "T_TIPO_DECIMAL", "texto": "T_TIPO_TEXTO",
    "si": "T_SI", "sino": "T_SINO", "entonces": "T_ENTONCES", "fin_si": "T_FIN_SI",
    "mientras": "T_MIENTRAS", "hacer": "T_HACER", "fin_mientras": "T_FIN_MIENTRAS",
    "imprimir": "T_IMPRIMIR", "Y": "T_OP_LOG", "O": "T_OP_LOG", "NO": "T_OP_LOG"
}

# Se regresó T_ID a la forma original que NO permite guiones bajos internos
tokens_regex = [
    ("T_DECIMAL", r'[+-]?\d+\.\d+'),
    ("T_ENTERO", r'[+-]?\d+'),
    ("T_CADENA", r'"[^"]*"'),
    ("T_OP_REL", r'>=|<=|==|!=|>|<'),
    ("T_OP_ARIT", r'\+|-|\*|/|='),
    ("T_ID", r'[a-zA-Z][a-zA-Z0-9]*'), 
    ("T_PARENTESIS", r'\(|\)')
]

def identificar_y_sugerir(simbolo, linea_completa):
    """Analiza por qué el token falló según las reglas originales."""
    
    # Caso: Intento de usar guion bajo (como en fin_si)
    if simbolo == "_":
        if "fin" in linea_completa and "si" in linea_completa:
            return "Error en palabra reservada: El lenguaje usa 'fin_si' como un token especial, pero tu regla de ID no permite guiones. Revisa la definicion de reservadas."
        return "El guion bajo '_' no esta permitido en los identificadores segun las reglas actuales."
    
    # Caso: Identificador que empieza con número
    if simbolo.isdigit():
        # Verificamos si lo que sigue es una letra (intento de ID inválido)
        return "Los identificadores deben comenzar con una letra. No se permiten digitos al inicio."
    
    # Caso: Símbolos de otros lenguajes
    if simbolo in ['@', '#', '$', ';', '{', '}']:
        return f"El simbolo '{simbolo}' es ajeno a la sintaxis de SimplePy. Por favor, eliminalo."
    
    # Caso: Cadena mal cerrada
    if simbolo == '"':
        return "Cadena de texto sin cerrar. Asegurate de usar comillas dobles al final."

    return "Caracter no reconocido. Revisa espacios o caracteres especiales no permitidos."

def analizar(codigo):
    tokens, errores = [], []
    lineas = codigo.split("\n")
    contador = 1
    lineas_con_error = set()
    
    for num_linea, linea in enumerate(lineas, start=1):
        linea_p = re.sub(r'//.*', '', linea) 
        pos = 0
        while pos < len(linea_p):
            if re.match(r'\s', linea_p[pos]):
                pos += 1
                continue
            
            match = None
            for tipo, regex in tokens_regex:
                patron = re.compile(regex)
                match = patron.match(linea_p, pos)
                if match:
                    lexema = match.group(0)
                    if tipo == "T_ID" and lexema in reservadas:
                        tipo = reservadas[lexema]
                    tokens.append({"N°": contador, "Lexema": lexema, "Token": tipo})
                    contador += 1
                    pos = match.end(0)
                    break
            
            if not match:
                simbolo_err = linea_p[pos]
                # Aquí identificamos el error sin haber cambiado el token regex
                sugerencia = identificar_y_sugerir(simbolo_err, linea)
                errores.append({
                    "Linea": num_linea,
                    "Simbolo": simbolo_err,
                    "Mensaje": "Error Lexico",
                    "Sugerencia": sugerencia
                })
                lineas_con_error.add(num_linea)
                pos += 1
    return tokens, errores, lineas_con_error

# --- INTERFAZ ---
with st.sidebar:
    st.title("Controles")
    if st.button("Limpiar Todo"):
        st.session_state.codigo_master = ""
        st.session_state.reset_key += 1
        st.rerun()
    st.markdown("---")
    st.subheader("Historial")
    for i, item in enumerate(reversed(st.session_state.historial)):
        with st.expander(f"Sesion {item['fecha']}"):
            st.markdown(f'<div class="scroll-history">{item["codigo"]}</div>', unsafe_allow_html=True)
            if st.button("Cargar", key=f"h_{i}"):
                st.session_state.codigo_master = item['codigo']
                st.session_state.reset_key += 1
                st.rerun()

st.header("SimplePy Engine")

def sync_codigo():
    st.session_state.codigo_master = st.session_state[f"ed_{st.session_state.reset_key}"]

codigo_actual = st.text_area(
    "Editor de Codigo", height=250, 
    value=st.session_state.codigo_master,
    key=f"ed_{st.session_state.reset_key}",
    on_change=sync_codigo
)

if st.button("Traducir"):
    txt = st.session_state.codigo_master
    if txt.strip():
        tokens, errores, l_error = analizar(txt)
        st.session_state.historial.append({"fecha": datetime.now().strftime("%H:%M:%S"), "codigo": txt})

        if errores:
            st.subheader("Diagnostico de Errores")
            output = '<div style="background-color: #0d1117; padding:10px; border-radius:8px; border:1px solid #30363d;">'
            for i, line in enumerate(txt.split('\n'), 1):
                css = "line-error" if i in l_error else ""
                output += f'<div class="code-line {css}"><span class="line-number">{i}</span>{line}</div>'
            st.markdown(output + '</div>', unsafe_allow_html=True)

        t1, t2 = st.tabs(["Tabla de Simbolos", "Reporte Detallado"])
        with t1:
            if tokens: st.dataframe(pd.DataFrame(tokens), use_container_width=True, hide_index=True)
        with t2:
            if errores: st.table(pd.DataFrame(errores))
            else: st.success("Codigo validado correctamente.")
    else:
        st.warning("El editor esta vacio.")