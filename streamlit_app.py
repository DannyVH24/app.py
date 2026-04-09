import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os

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
    
    .main-footer {
        margin-top: 150px;
        padding: 20px;
        border-top: 1px solid #30363d;
        text-align: center;
        color: #8b949e;
        font-size: 0.9em;
    }
    .dev-name { color: #58a6ff; font-weight: bold; }
    
    .logo-frame {
        border: 2px solid #30363d;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        background-color: rgba(48, 54, 61, 0.2);
    }
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- SUGERENCIA (PLACEHOLDER) ---
sugerencia_ejemplo = """// Prueba aquí tus casos válidos o inválidos
entero variable = 10
texto msj = "Hola"
// Ejemplo de error:
entero 1variable = 5"""

# --- ESTADO DE SESIÓN ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0
if 'codigo_master' not in st.session_state: st.session_state.codigo_master = ""

# --- MOTOR LÉXICO ---
reservadas = {
    "entero": "T_TIPO_ENTERO", "decimal": "T_TIPO_DECIMAL", "texto": "T_TIPO_TEXTO",
    "si": "T_SI", "sino": "T_SINO", "entonces": "T_ENTONCES", "fin_si": "T_FIN_SI",
    "mientras": "T_MIENTRAS", "hacer": "T_HACER", "fin_mientras": "T_FIN_MIENTRAS",
    "revisar": "T_REVISAR", "imprimir": "T_IMPRIMIR",
    "Y": "T_OP_LOG", "O": "T_OP_LOG", "NO": "T_OP_LOG"
}

# Modificamos REGEX para evitar que números "absorban" parte de identificadores inválidos
tokens_regex = [
    ("T_COMENTARIO", r'(//.*|#.*)'),             
    ("T_DECIMAL", r'[+-]?[0-9]+\.[0-9]+'),       
    ("T_ENTERO", r'[+-]?[0-9]+'),                
    ("T_CADENA", r'"[^"\n]*"'),                    
    ("T_OP_REL", r'>=|<=|==|!=|>|<'),            
    ("T_OP_ARIT", r'\+|-|\*|/|='),               
    ("T_ID", r'[a-zA-Z][a-zA-Z0-9_]*'),           
    ("T_PARENTESIS", r'\(|\)')
]

def identificar_y_sugerir(simbolo, linea_restante):
    """Diagnóstico detallado para el reporte estructurado"""
    # Caso específico para Regla 6.1: Si empieza con número pero le siguen letras
    if simbolo.isdigit() and any(c.isalpha() for c in linea_restante.split()[0] if linea_restante.strip()):
        return "MOTIVO: Los identificadores deben iniciar con una letra. Violación de la Regla 6.1."
    
    if simbolo.isdigit():
        return "MOTIVO: Error de formación numérica o identificador mal declarado. Violación de la Regla 6.1 / 6.2."
    
    if simbolo == '"':
        return "MOTIVO: Apertura de cadena sin cierre. Las cadenas no pueden abarcar múltiples líneas. Violación de la Regla 6.4."
        
    if re.match(r'\d*\.\.', simbolo + linea_restante):
        return "MOTIVO: Estructura numérica inválida (doble punto decimal). Violación de la Regla 6.3."
        
    if simbolo in "$%&|?¿¡!":
        return f"MOTIVO: El carácter '{simbolo}' no pertenece al alfabeto de SimplePy. Violación de la Regla 6.10."
        
    return "MOTIVO: Secuencia de caracteres no reconocida por las reglas del lenguaje."

def analizar(codigo):
    tokens, errores = [], []
    lineas = codigo.split("\n")
    contador = 1
    lineas_con_error = set()
    
    for num_linea, linea in enumerate(lineas, start=1):
        pos = 0
        while pos < len(linea):
            # Ignorar espacios (Regla 6.9)
            if linea[pos].isspace():
                pos += 1
                continue
                
            match = None
            for tipo, regex in tokens_regex:
                patron = re.compile(regex)
                match = patron.match(linea, pos)
                if match:
                    lexema = match.group(0)
                    
                    # --- VALIDACIÓN CRÍTICA REGLA 6.1 ---
                    # Si detectamos un número, revisamos si el carácter inmediatamente posterior es una letra
                    if tipo in ["T_ENTERO", "T_DECIMAL"]:
                        fin_lexema = pos + len(lexema)
                        if fin_lexema < len(linea) and (linea[fin_lexema].isalpha() or linea[fin_lexema] == '_'):
                            # Es un error: Identificador empezando con número (ej: 1variable)
                            match = None # Forzamos a que no haya match para que caiga en el bloque de error
                            break 
                    
                    # Si el ID es en realidad una palabra reservada
                    if tipo == "T_ID" and lexema in reservadas:
                        tipo = reservadas[lexema]
                    
                    if tipo != "T_COMENTARIO":
                        tokens.append({"N°": contador, "Lexema": lexema, "Token": tipo, "Linea": num_linea})
                        contador += 1
                    pos = match.end(0)
                    break
            
            if not match:
                simbolo_err = linea[pos]
                # Capturamos un poco más de contexto para la sugerencia
                contexto_error = linea[pos+1:pos+10]
                errores.append({
                    "Linea": num_linea, 
                    "Simbolo": simbolo_err, 
                    "Sugerencia del Error": identificar_y_sugerir(simbolo_err, contexto_error)
                })
                lineas_con_error.add(num_linea)
                pos += 1
                
    return tokens, errores, lineas_con_error

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
    ruta_logo = "img/img-1.png" if os.path.exists("img/img-1.png") else "img-1.png"
    if os.path.exists(ruta_logo): 
        st.image(ruta_logo, use_container_width=True)
    else: 
        st.subheader("SimplePy IDE")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Controles")
    if st.button("Limpiar Todo"):
        st.session_state.codigo_master = ""
        st.session_state.reset_key += 1
        st.rerun()
        
    st.markdown("---")
    st.subheader("Historial de Sesiones")
    for i, item in enumerate(reversed(st.session_state.historial)):
        with st.expander(f"Sesion {item['fecha']}"):
            st.code(item['codigo'], language="python")
            if st.button("Cargar", key=f"btn_{i}"):
                st.session_state.codigo_master = item['codigo']
                st.session_state.reset_key += 1
                st.rerun()

# --- ÁREA PRINCIPAL ---
st.header("SimplePy Engine")

def sync_codigo():
    st.session_state.codigo_master = st.session_state[f"ed_{st.session_state.reset_key}"]

codigo_actual = st.text_area(
    "Editor de Codigo", height=250, 
    value=st.session_state.codigo_master,
    placeholder=sugerencia_ejemplo,
    key=f"ed_{st.session_state.reset_key}",
    on_change=sync_codigo
)

if st.button("Traducir"):
    txt = st.session_state.codigo_master
    if txt.strip():
        tokens, errores, l_error = analizar(txt)
        if not st.session_state.historial or st.session_state.historial[-1]['codigo'] != txt:
            st.session_state.historial.append({"fecha": datetime.now().strftime("%H:%M:%S"), "codigo": txt})
        
        if errores:
            st.subheader("⚠️ Diagnóstico de Errores")
            output = '<div style="background-color: #0d1117; padding:10px; border-radius:8px; border:1px solid #30363d;">'
            for j, line in enumerate(txt.split('\n'), 1):
                css = "line-error" if j in l_error else ""
                output += f'<div class="code-line {css}"><span class="line-number">{j}</span>{line}</div>'
            st.markdown(output + '</div>', unsafe_allow_html=True)

        t1, t2 = st.tabs(["Tabla de Símbolos", "Reporte Detallado de Errores"])
        with t1:
            if tokens: st.dataframe(pd.DataFrame(tokens), use_container_width=True, hide_index=True)
        with t2:
            if errores: 
                st.table(pd.DataFrame(errores))
            else: 
                st.success("Análisis léxico completado sin errores. El código cumple con todas las reglas.")
    else:
        st.warning("El editor está vacío.")

# --- FOOTER ---
st.markdown(f"""
    <div class="main-footer">
        <p>© 2026 SimplePy Engine. Facultad de Ingeniería.</p>
        <p>Desarrollado por: <span class="dev-name">Danny Velásquez</span> & <span class="dev-name">André Herrera</span></p>
    </div>
""", unsafe_allow_html=True)