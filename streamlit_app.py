import streamlit as st
import numpy as np

# Estilos personalizados
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4A90E2;
        }
        .container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        .card {
            width: 400px;
            height: 400px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 20px;
            cursor: pointer;
            transition: 0.3s;
        }
        .card:hover {
            background-color: #e0e0e0;
        }
        .project-description {
            text-align: center;
            font-size: 18px;
            margin-top: 20px;
            padding: 15px;
            background-color: #eef1f7;
            border-radius: 10px;
            color: black;
        }
        .section {
            margin-top: 30px;
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
        }
        .submenu {
            margin: 15px 0;
            padding: 10px;
            background-color: #e3e8f0;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title">Calculadora Estadística 📊</div>', unsafe_allow_html=True)

# Descripción del Proyecto
st.markdown('<div class="project-description">Esta aplicación permite calcular diferentes parámetros estadísticos. Selecciona una opción para comenzar.</div>', unsafe_allow_html=True)

# Contenedor de opciones principales
st.markdown('<div class="container">', unsafe_allow_html=True)

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

if st.session_state["main_menu"] == "Estadística 1":
    st.subheader("📘 Estadística 1")
    st.write("Contenido de Estadística 1 (por implementar)")

elif st.session_state["main_menu"] == "Estadística 2":
    st.subheader("📗 Estadística 2")
    
    # Submenú para Estadística 2
    st.markdown('<div class="submenu">', unsafe_allow_html=True)
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        if st.button("Intervalos de Confianza", key="intervalos"):
            st.session_state["sub_menu"] = "Intervalos de Confianza"
    
    with sub_col2:
        if st.button("Tamaños de Muestra", key="tamanos"):
            st.session_state["sub_menu"] = "Tamaños de Muestra"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenido de Estadística 2
    if "sub_menu" not in st.session_state:
        st.session_state["sub_menu"] = None
    
    if st.session_state["sub_menu"] == "Intervalos de Confianza":
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("Intervalos de Confianza")
        
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
            z = st.number_input("Valor Z (nivel de confianza)", value=1.960, format="%.3f", step=0.001)
            
            if st.button("Calcular"):
                margen_error = z * (sigma / np.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.success(f"Intervalo de confianza: ({li:.4f}, {ls:.4f})")
        
        elif opcion == "Intervalo para la media (σ desconocida)":
            media = st.number_input("Media muestral", value=50.0)
            s = st.number_input("Desviación estándar muestral (s)", value=10.0)
            n = st.number_input("Tamaño de muestra (n)", value=30)
            t = st.number_input("Valor t (nivel de confianza)", value=2.045, format="%.3f", step=0.001)
            
            if st.button("Calcular"):
                margen_error = t * (s / np.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.success(f"Intervalo de confianza: ({li:.4f}, {ls:.4f})")
        
        elif opcion == "Intervalo para la media (muestra pequeña)":
            media = st.number_input("Media muestral", value=50.0)
            s = st.number_input("Desviación estándar muestral (s)", value=10.0)
            n = st.number_input("Tamaño de muestra (n)", value=10)
            t = st.number_input("Valor t (nivel de confianza)", value=2.262, format="%.3f", step=0.001)
            
            if st.button("Calcular"):
                margen_error = t * (s / np.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.success(f"Intervalo de confianza: ({li:.4f}, {ls:.4f})")
        
        elif opcion == "Intervalo para la proporción":
            p = st.number_input("Proporción muestral (p)", value=0.50, format="%.3f")
            n = st.number_input("Tamaño de muestra (n)", value=100)
            z = st.number_input("Valor Z (nivel de confianza)", value=1.960, format="%.3f", step=0.001)
            
            if st.button("Calcular"):
                margen_error = z * np.sqrt((p * (1 - p)) / n)
                li = p - margen_error
                ls = p + margen_error
                st.success(f"Intervalo de confianza: ({li:.4f}, {ls:.4f})")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state["sub_menu"] == "Tamaños de Muestra":
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("Tamaños de Muestra")
        
        opcion = st.selectbox("Selecciona el tipo de cálculo:", [
            "Población desconocida (proporciones)",
            "Población conocida (proporciones)",
            "Población desconocida (medias)",
            "Población conocida (medias)",
            "Ajuste por pérdidas"
        ])
        
        if opcion == "Población desconocida (proporciones)":
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f", step=0.001)
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                n = (Z**2 * p * (1-p)) / (d**2)
                st.success(f"**Tamaño de muestra necesario:** {round(n)}")
        
        elif opcion == "Población conocida (proporciones)":
            N = st.number_input("Tamaño población (N)", value=1000)
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f", step=0.001)
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                num = N * (Z**2 * p * (1-p))
                den = (d**2 * (N - 1)) + (Z**2 * p * (1-p))
                n = num / den
                st.success(f"**Tamaño de muestra necesario:** {round(n)}")
        
        elif opcion == "Población desconocida (medias)":
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f", step=0.001)
            s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                n = (Z**2 * s**2) / (d**2)
                st.success(f"**Tamaño de muestra necesario:** {round(n)}")
        
        elif opcion == "Población conocida (medias)":
            N = st.number_input("Tamaño población (N)", value=1000)
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f", step=0.001)
            s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")
            
            if st.button("Calcular"):
                num = N * (Z**2 * s**2)
                den = (d**2 * (N - 1)) + (Z**2 * s**2)
                n = num / den
                st.success(f"**Tamaño de muestra necesario:** {round(n)}")
        
        elif opcion == "Ajuste por pérdidas":
            n = st.number_input("Tamaño inicial (n)", value=100)
            pe = st.number_input("Pérdidas esperadas (decimal)", value=0.100, format="%.3f")
            
            if st.button("Calcular"):
                nc = n / (1 - pe)
                st.success(f"**Tamaño ajustado:** {round(nc)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
