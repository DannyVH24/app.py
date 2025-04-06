import streamlit as st
import numpy as np
import pandas as pd
import math

# Configuración de página
st.set_page_config(layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4A90E2;
            margin-bottom: 20px;
        }
        .project-description {
            text-align: center;
            font-size: 18px;
            padding: 15px;
            background-color: #eef1f7;
            border-radius: 10px;
            color: black;
            margin-bottom: 30px;
        }
        .main-menu {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .submenu-container {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .submenu {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        .sub-btn {
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
            background-color: white;
            border: 1px solid #e0e0e0;
        }
        .sub-btn:hover {
            background-color: #f0f4ff;
            transform: translateY(-1px);
        }
        .sub-btn.active {
            background-color: #4A90E2;
            color: white;
            border-color: #4A90E2;
        }
        .section {
            background-color: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0;
        }
        .data-table {
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        .result-box {
            background-color: #000000;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border-left: 4px solid #4A90E2;
        }
    </style>
""", unsafe_allow_html=True)

# Funciones para valores críticos
def get_z_value(confidence):
    z_table = {80: 1.282, 85: 1.440, 90: 1.645, 95: 1.960, 99: 2.576}
    return z_table.get(confidence, 1.960)

def get_t_value(confidence, df):
    t_table = {
        95: {1:12.706, 2:4.303, 3:3.182, 4:2.776, 5:2.571, 6:2.447, 7:2.365, 8:2.306, 9:2.262, 10:2.228},
        99: {1:63.657, 2:9.925, 3:5.841, 4:4.604, 5:4.032, 6:3.707, 7:3.499, 8:3.355, 9:3.250, 10:3.169}
    }
    return t_table.get(confidence, {}).get(min(df, 10), 2.0)

# Título principal
st.markdown('<div class="title">Calculadora Estadística 📊</div>', unsafe_allow_html=True)

# Descripción del Proyecto
st.markdown('<div class="project-description">Esta aplicación permite calcular diferentes parámetros estadísticos. Selecciona una opción para comenzar.</div>', unsafe_allow_html=True)

# Contenedor de opciones principales
st.markdown('<div class="main-menu">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("📘 Estadística 1", key="estadistica1"):
        st.session_state["main_menu"] = "Estadística 1"

with col2:
    if st.button("📗 Estadística 2", key="estadistica2"):
        st.session_state["main_menu"] = "Estadística 2"

st.markdown('</div>', unsafe_allow_html=True)

# Manejo de selección de menú principal
if "main_menu" not in st.session_state:
    st.session_state["main_menu"] = "Inicio"
    st.session_state["sub_menu"] = None
    st.session_state["generated_data"] = None
    st.session_state["data_params"] = {}

if st.session_state["main_menu"] == "Estadística 1":
    st.subheader("📘 Estadística 1")
    st.write("Contenido de Estadística 1 (por implementar)")

elif st.session_state["main_menu"] == "Estadística 2":
    st.subheader("📗 Estadística 2")
    
    # Submenú para Estadística 2 (ahora con 5 opciones)
    st.markdown('<div class="submenu-container">', unsafe_allow_html=True)
    st.markdown('<div class="submenu">', unsafe_allow_html=True)
    
    sub_options = {
        "📏 Intervalos": "Intervalos de Confianza",
        "🔍 Tamaños Muestra": "Tamaños de Muestra",
        "📊 Generar Datos": "Generar Datos",
        "📈 Est. con Datos": "Estimación con Datos"
    }
    
    for label, key in sub_options.items():
        if st.button(label, key=key):
            st.session_state["sub_menu"] = key
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenido de Estadística 2
    if "sub_menu" not in st.session_state:
        st.session_state["sub_menu"] = None
    
    # 1. Sección original de Intervalos de Confianza
    if st.session_state["sub_menu"] == "Intervalos de Confianza":
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("📏 Intervalos de Confianza")
        
        opcion = st.selectbox("Selecciona el tipo de intervalo:", [
            "Intervalo para la media (σ conocida)",
            "Intervalo para la media (σ desconocida)",
            "Intervalo para la media (muestra pequeña)",
            "Intervalo para la proporción"
        ])
        
        if opcion == "Intervalo para la media (σ conocida)":
            media = st.number_input("Media muestral", value=50.0)
            sigma = st.number_input("Desviación estándar poblacional (σ)", value=10.0)
            n = st.number_input("Tamaño de muestra (n)", value=30)
            confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
            z = get_z_value(confianza)
            
            if st.button("Calcular"):
                margen_error = z * (sigma / math.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.markdown(f'<div class="result-box">Intervalo de confianza al {confianza}%: <strong>({li:.4f}, {ls:.4f})</strong></div>', unsafe_allow_html=True)
        
        elif opcion == "Intervalo para la media (σ desconocida)":
            media = st.number_input("Media muestral", value=50.0)
            s = st.number_input("Desviación estándar muestral (s)", value=10.0)
            n = st.number_input("Tamaño de muestra (n)", value=30)
            confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
            t_val = get_t_value(confianza, n-1)
            
            if st.button("Calcular"):
                margen_error = t_val * (s / math.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.markdown(f'<div class="result-box">Intervalo de confianza al {confianza}%: <strong>({li:.4f}, {ls:.4f})</strong></div>', unsafe_allow_html=True)
        
        elif opcion == "Intervalo para la media (muestra pequeña)":
            media = st.number_input("Media muestral", value=50.0)
            s = st.number_input("Desviación estándar muestral (s)", value=10.0)
            n = st.number_input("Tamaño de muestra (n)", value=10)
            confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
            t_val = get_t_value(confianza, n-1)
            
            if st.button("Calcular"):
                margen_error = t_val * (s / math.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.markdown(f'<div class="result-box">Intervalo de confianza al {confianza}%: <strong>({li:.4f}, {ls:.4f})</strong></div>', unsafe_allow_html=True)
        
        elif opcion == "Intervalo para la proporción":
            p = st.number_input("Proporción muestral (p)", value=0.50, format="%.3f")
            n = st.number_input("Tamaño de muestra (n)", value=100)
            confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
            z = get_z_value(confianza)
            
            if st.button("Calcular"):
                margen_error = z * math.sqrt((p * (1 - p)) / n)
                li = p - margen_error
                ls = p + margen_error
                st.markdown(f'<div class="result-box">Intervalo de confianza al {confianza}%: <strong>({li:.4f}, {ls:.4f})</strong></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Sección original de Tamaños de Muestra
    elif st.session_state["sub_menu"] == "Tamaños de Muestra":
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("🔍 Tamaños de Muestra")
        
        opcion = st.selectbox("Selecciona el tipo de cálculo:", [
            "Población desconocida (proporciones)",
            "Población conocida (proporciones)",
            "Población desconocida (medias)",
            "Población conocida (medias)",
            "Ajuste por pérdidas"
        ])
        
        confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
        Z = get_z_value(confianza)
        
        if opcion == "Población desconocida (proporciones)":
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                n = (Z**2 * p * (1-p)) / (d**2)
                st.markdown(f'<div class="result-box">Tamaño de muestra necesario: <strong>{math.ceil(n)}</strong></div>', unsafe_allow_html=True)
        
        elif opcion == "Población conocida (proporciones)":
            N = st.number_input("Tamaño población (N)", value=1000)
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                num = N * (Z**2 * p * (1-p))
                den = (d**2 * (N - 1)) + (Z**2 * p * (1-p))
                n = num / den
                st.markdown(f'<div class="result-box">Tamaño de muestra necesario: <strong>{math.ceil(n)}</strong> ({(math.ceil(n)/N*100):.1f}% de la población)</div>', unsafe_allow_html=True)
        
        elif opcion == "Población desconocida (medias)":
            s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                n = (Z**2 * s**2) / (d**2)
                st.markdown(f'<div class="result-box">Tamaño de muestra necesario: <strong>{math.ceil(n)}</strong></div>', unsafe_allow_html=True)
        
        elif opcion == "Población conocida (medias)":
            N = st.number_input("Tamaño población (N)", value=1000)
            s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                num = N * (Z**2 * s**2)
                den = (d**2 * (N - 1)) + (Z**2 * s**2)
                n = num / den
                st.markdown(f'<div class="result-box">Tamaño de muestra necesario: <strong>{math.ceil(n)}</strong> ({(math.ceil(n)/N*100):.1f}% de la población)</div>', unsafe_allow_html=True)
        
        elif opcion == "Ajuste por pérdidas":
            n = st.number_input("Tamaño inicial (n)", value=100)
            pe = st.number_input("Pérdidas esperadas (decimal)", value=0.100, format="%.3f")
            
            if st.button("Calcular"):
                nc = n / (1 - pe)
                st.markdown(f'<div class="result-box">Tamaño ajustado: <strong>{math.ceil(nc)}</strong></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Nueva sección para Generar Datos
    elif st.session_state["sub_menu"] == "Generar Datos":
        with st.container():
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("📊 Generador de Datos Aleatorios")
            
            col1, col2 = st.columns(2)
            with col1:
                n_datos = st.number_input("Número de datos", min_value=1, max_value=1000, value=30)
                decimales = st.number_input("Decimales", min_value=0, max_value=6, value=2)
            with col2:
                min_val = st.number_input("Valor mínimo", value=0.0)
                max_val = st.number_input("Valor máximo", value=100.0)
            
            if st.button("Generar Datos"):
                if min_val >= max_val:
                    st.error("El valor mínimo debe ser menor que el valor máximo")
                else:
                    datos_aleatorios = np.random.uniform(min_val, max_val, n_datos)
                    datos_redondeados = np.round(datos_aleatorios, decimales)
                    
                    st.session_state.generated_data = pd.DataFrame({
                        "ID": range(1, n_datos+1),
                        "Valor": datos_redondeados
                    })
                    
                    # Calcular parámetros poblacionales
                    st.session_state.data_params = {
                        "media_poblacional": np.mean(datos_aleatorios),
                        "desv_poblacional": np.std(datos_aleatorios),
                        "n_datos": n_datos
                    }
                    
                    st.success("Datos generados exitosamente!")
            
            if st.session_state.generated_data is not None:
                st.dataframe(st.session_state.generated_data, height=400, use_container_width=True)
                
                st.markdown(f'''
                <div class="result-box">
                    <p><strong>Parámetros poblacionales:</strong></p>
                    <p>Media poblacional: {st.session_state.data_params["media_poblacional"]:.4f}</p>
                    <p>Desviación estándar poblacional: {st.session_state.data_params["desv_poblacional"]:.4f}</p>
                    <p>Tamaño de la población: {st.session_state.data_params["n_datos"]}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Opción para descargar
                csv = st.session_state.generated_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Descargar CSV",
                    csv,
                    "datos_aleatorios.csv",
                    "text/csv",
                    key='download-csv'
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. Nueva sección para Estimación con Datos Generados
    elif st.session_state["sub_menu"] == "Estimación con Datos":
        with st.container():
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("📈 Análisis con Datos Generados")
            
            if st.session_state.generated_data is None:
                st.warning("Primero genera datos en la sección 'Generar Datos'")
            else:
                datos = st.session_state.generated_data["Valor"].values
                n = len(datos)
                media = np.mean(datos)
                desv = np.std(datos, ddof=1)
                
                st.markdown(f'''
                <div class="result-box">
                    <p><strong>Estadísticos descriptivos:</strong></p>
                    <p>Media muestral: {media:.4f}</p>
                    <p>Desviación estándar muestral: {desv:.4f}</p>
                    <p>Tamaño de muestra: {n}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Opciones de análisis
                analisis = st.selectbox("Selecciona el tipo de análisis:", [
                    "Estimación de Media",
                    "Tamaño de Muestra para Media",
                    "Estimación de Proporción",
                    "Tamaño de Muestra para Proporción"
                ])
                
                confianza = st.selectbox("Nivel de confianza", [90, 95, 99], index=1)
                
                if analisis == "Estimación de Media":
                    if st.button("Calcular Intervalo de Confianza"):
                        if n >= 30:
                            z = get_z_value(confianza)
                            margen_error = z * (desv / math.sqrt(n))
                        else:
                            t_val = get_t_value(confianza, n-1)
                            margen_error = t_val * (desv / math.sqrt(n))
                        
                        li = media - margen_error
                        ls = media + margen_error
                        
                        st.markdown(f'''
                        <div class="result-box">
                            <p><strong>Intervalo de confianza al {confianza}% para la media:</strong></p>
                            <p>({li:.4f}, {ls:.4f})</p>
                            <p><strong>Margen de error:</strong> ±{margen_error:.4f}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                
                elif analisis == "Tamaño de Muestra para Media":
                    error = st.number_input("Margen de error deseado", value=5.0, step=0.1)
                    
                    if st.button("Calcular Tamaño de Muestra"):
                        N = st.session_state.data_params["n_datos"]
                        s = st.session_state.data_params["desv_poblacional"]
                        Z = get_z_value(confianza)
                        
                        num = N * (Z**2 * s**2)
                        den = (error**2 * (N - 1)) + (Z**2 * s**2)
                        n_necesario = num / den
                        
                        st.markdown(f'''
                        <div class="result-box">
                            <p><strong>Tamaño de muestra necesario:</strong></p>
                            <p>Para estimar la media con un error de ±{error} y {confianza}% de confianza: <strong>{math.ceil(n_necesario)}</strong></p>
                            <p>Representa el <strong>{(math.ceil(n_necesario)/N*100):.1f}%</strong> de la población</p>
                        </div>
                        ''', unsafe_allow_html=True)
                
                elif analisis == "Estimación de Proporción":
                    exitos = st.number_input("Número de éxitos observados", min_value=0, max_value=n, value=int(n/2))
                    
                    if st.button("Calcular Intervalo de Proporción"):
                        p_hat = exitos / n
                        z = get_z_value(confianza)
                        margen_error = z * math.sqrt((p_hat * (1 - p_hat)) / n)
                        li = p_hat - margen_error
                        ls = p_hat + margen_error
                        
                        st.markdown(f'''
                        <div class="result-box">
                            <p><strong>Intervalo de confianza al {confianza}% para la proporción:</strong></p>
                            <p>({li:.4f}, {ls:.4f})</p>
                            <p><strong>Proporción muestral:</strong> {p_hat:.4f}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                
                elif analisis == "Tamaño de Muestra para Proporción":
                    p_esperada = st.number_input("Proporción esperada", value=0.5, min_value=0.0, max_value=1.0, step=0.01)
                    error = st.number_input("Margen de error deseado", value=0.05, min_value=0.01, max_value=0.5, step=0.01)
                    
                    if st.button("Calcular Tamaño de Muestra"):
                        N = st.session_state.data_params["n_datos"]
                        Z = get_z_value(confianza)
                        
                        num = N * (Z**2 * p_esperada * (1-p_esperada))
                        den = (error**2 * (N - 1)) + (Z**2 * p_esperada * (1-p_esperada))
                        n_necesario = num / den
                        
                        st.markdown(f'''
                        <div class="result-box">
                            <p><strong>Tamaño de muestra necesario:</strong></p>
                            <p>Para estimar la proporción con un error de ±{error} y {confianza}% de confianza: <strong>{math.ceil(n_necesario)}</strong></p>
                            <p>Representa el <strong>{(math.ceil(n_necesario)/N*100):.1f}%</strong> de la población</p>
                        </div>
                        ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
