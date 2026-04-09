import streamlit as st
import re
import pandas as pd

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(page_title="SimplePy IDE", layout="wide")

# =========================
# PALABRAS RESERVADAS
# =========================
reservadas = {
    "entero": "T_TIPO_ENTERO",
    "decimal": "T_TIPO_DECIMAL",
    "texto": "T_TIPO_TEXTO",
    "si": "T_SI",
    "sino": "T_SINO",
    "entonces": "T_ENTONCES",
    "fin_si": "T_FIN_SI",
    "mientras": "T_MIENTRAS",
    "hacer": "T_HACER",
    "fin_mientras": "T_FIN_MIENTRAS",
    "imprimir": "T_IMPRIMIR",
    "Y": "T_OP_LOG",
    "O": "T_OP_LOG",
    "NO": "T_OP_LOG"
}

# =========================
# TOKENS REGEX
# =========================
tokens_regex = [
    ("T_DECIMAL", r'[+-]?\d+\.\d+'),
    ("T_ENTERO", r'[+-]?\d+'),
    ("T_CADENA", r'"[^"]*"'),
    ("T_OP_REL", r'>=|<=|==|!=|>|<'),
    ("T_OP_ARIT", r'\+|-|\*|/|='),
    ("T_ID", r'[a-zA-Z][a-zA-Z0-9]*'),
    ("T_PARENTESIS", r'\(|\)')
]

# =========================
# ANALIZADOR LÓGICO
# =========================
def analizar(codigo):
    tokens = []
    errores = []
    contador = 1
    lineas = codigo.split("\n")

    for num_linea, linea in enumerate(lineas, start=1):
        linea_limpia = re.sub(r'//.*', '', linea)
        pos = 0

        while pos < len(linea_limpia):
            if re.match(r'\s', linea_limpia[pos]):
                pos += 1
                continue

            match = None
            for tipo, regex in tokens_regex:
                patron = re.compile(regex)
                match = patron.match(linea_limpia, pos)

                if match:
                    lexema = match.group(0)
                    if tipo == "T_ID" and lexema in reservadas:
                        tipo = reservadas[lexema]

                    tokens.append({"N°": contador, "Lexema": lexema, "Token": tipo})
                    contador += 1
                    pos = match.end(0)
                    break

            if not match:
                errores.append({
                    "N°": len(errores) + 1,
                    "Descripción": f"Línea {num_linea}",
                    "Detalle": f"Símbolo inválido: '{linea_limpia[pos]}'",
                    "Sugerencia": "Verifica el carácter"
                })
                pos += 1

    return tokens, errores

# =========================
# INTERFAZ STREAMLIT
# =========================
st.title("🚀 SimplePy IDE - Analizador Léxico")

# Sidebar para controles
with st.sidebar:
    st.header("Controles")
    btn_limpiar = st.button("🧹 Limpiar Todo")
    st.info("Escribe tu código en el editor central y presiona 'Traducir'.")

# Editor de Código
if btn_limpiar:
    st.session_state.codigo_input = ""

codigo_input = st.text_area(
    "Código SimplePy", 
    placeholder="Escribe tu código aquí...", 
    height=250,
    key="editor"
)

col1, col2 = st.columns([1, 5])
with col1:
    ejecutar = st.button("▶ Traducir", type="primary")

# Lógica de ejecución
if ejecutar and codigo_input:
    tokens, errores = analizar(codigo_input)

    # Mostrar Resultados
    st.divider()
    
    tab1, tab2 = st.tabs(["📊 Tabla de Símbolos", "⚠️ Errores Léxicos"])

    with tab1:
        if tokens:
            df_tokens = pd.DataFrame(tokens)
            st.dataframe(df_tokens, use_container_width=True, hide_index=True)
        else:
            st.write("No se encontraron tokens.")

    with tab2:
        if errores:
            st.error("Se detectaron errores en el código.")
            df_errores = pd.DataFrame(errores)
            st.table(df_errores)
        else:
            st.success("¡Código limpio! No se encontraron errores léxicos.")

elif ejecutar and not codigo_input:
    st.warning("Por favor, ingresa algún código para analizar.")

# Footer estilo
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Source Code Pro', monospace;
        background-color: #262730;
        color: #00FF00;
    }
</style>
""", unsafe_allow_html=True)