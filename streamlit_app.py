import streamlit as st
import numpy as np
from scipy.stats import t, norm  # Importamos scipy.stats para cálculos estadísticos

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
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title">Calculadora Estadística 📊</div>', unsafe_allow_html=True)

# Descripción del Proyecto
st.markdown('<div class="project-description">Esta aplicación permite realizar cálculos estadísticos como tamaño de muestra e intervalos de confianza.</div>', unsafe_allow_html=True)

# Contenedor de opciones
st.markdown('<div class="container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("📘 Estadística 1", key="estadistica1"):
        st.session_state["menu"] = "Estadística 1"

with col2:
    if st.button("📗 Estadística 2", key="estadistica2"):
        st.session_state["menu"] = "Estadística 2"

st.markdown('</div>', unsafe_allow_html=True)

# Manejo de selección de menú
if "menu" not in st.session_state:
    st.session_state["menu"] = "Inicio"

if st.session_state["menu"] == "Estadística 1":
    st.subheader("📘 Estadística 1")
    st.write("Aquí irán los temas de Estadística 1.")

elif st.session_state["menu"] == "Estadística 2":
    st.subheader("📗 Estadística 2")

    # Menú dentro de Estadística 2
    submenu = st.selectbox("Selecciona una categoría:", ["Tamaño de muestra", "Intervalos de confianza"])

    # Tamaño de muestra
    if submenu == "Tamaño de muestra":
        opcion = st.selectbox("Selecciona el cálculo de tamaño de muestra:", [
            "Población desconocida",
            "Población conocida",
            "Estimación de medias (población desconocida)",
            "Estimación de medias (población conocida)",
            "Ajuste por pérdidas esperadas"
        ])

        if opcion == "Población desconocida":
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f")
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            q = 1 - p
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")

            if st.button("Calcular"):
                n = (Z**2 * p * q) / (d**2)
                st.write(f"**Tamaño de muestra necesario:** {round(n)}")

        elif opcion == "Población conocida":
            N = st.number_input("Tamaño de la población (N)", value=1000)
            Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f")
            p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
            q = 1 - p
            d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")

            if st.button("Calcular"):
                num = N * (Z**2 * p * q)
                den = (d**2 * (N - 1)) + (Z**2 * p * q)
                n = num / den
                st.write(f"**Tamaño de muestra necesario:** {round(n)}")

    # Intervalos de confianza
    elif submenu == "Intervalos de confianza":
        opcion_ic = st.selectbox("Selecciona el tipo de intervalo:", [
            "Intervalo para la media (σ conocida)",
            "Intervalo para la media (σ desconocida, muestra pequeña)"
        ])

        if opcion_ic == "Intervalo para la media (σ conocida)":
            st.subheader("Intervalo de confianza para la media (σ conocida)")
            media = st.number_input("Media muestral (x̄)", value=50.0, format="%.2f")
            sigma = st.number_input("Desviación estándar poblacional (σ)", value=5.0, format="%.2f")
            n = st.number_input("Tamaño de la muestra (n)", value=30, min_value=1)
            confianza = st.number_input("Nivel de confianza (%)", value=95, min_value=1, max_value=99)

            if st.button("Calcular"):
                alpha = 1 - (confianza / 100)
                Z = norm.ppf(1 - alpha/2)  # Valor crítico Z
                margen_error = Z * (sigma / np.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.write(f"**Intervalo de confianza:** ({li:.2f}, {ls:.2f})")

        elif opcion_ic == "Intervalo para la media (σ desconocida, muestra pequeña)":
            st.subheader("Intervalo de confianza para la media (σ desconocida)")
            media = st.number_input("Media muestral (x̄)", value=50.0, format="%.2f")
            s = st.number_input("Desviación estándar muestral (s)", value=5.0, format="%.2f")
            n = st.number_input("Tamaño de la muestra (n)", value=10, min_value=1)
            confianza = st.number_input("Nivel de confianza (%)", value=95, min_value=1, max_value=99)

            if st.button("Calcular"):
                alpha = 1 - (confianza / 100)
                gl = n - 1  # Grados de libertad
                t_critico = t.ppf(1 - alpha/2, gl)  # Valor crítico t
                margen_error = t_critico * (s / np.sqrt(n))
                li = media - margen_error
                ls = media + margen_error
                st.write(f"**Intervalo de confianza:** ({li:.2f}, {ls:.2f})")
