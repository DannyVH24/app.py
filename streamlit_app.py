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
       
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title">Calculadora Estadística 📊</div>', unsafe_allow_html=True)

# Descripción del Proyecto
st.markdown('<div class="project-description">Esta aplicación permite calcular el tamaño de muestra en diferentes escenarios estadísticos. Selecciona una opción para comenzar.</div>', unsafe_allow_html=True)

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

# Cuadro para texto del proyecto

# Manejo de selección de menú
if "menu" not in st.session_state:
    st.session_state["menu"] = "Inicio"

if st.session_state["menu"] == "Estadística 1":
    st.subheader("📘 Estadística 1")
    st.write("Aquí irán los temas de Estadística 1.")

elif st.session_state["menu"] == "Estadística 2":
    st.subheader("📗 Estadística 2")

    # Selección de la fórmula a usar en Estadística 2
    opcion = st.selectbox("Selecciona el cálculo a realizar:", [
        "Tamaño de muestra (población desconocida)",
        "Tamaño de muestra (población conocida)",
        "Tamaño de muestra para estimación de medias (población desconocida)",
        "Tamaño de muestra para estimación de medias (población conocida)",
        "Ajuste por pérdidas esperadas"
    ])

    # Entrada de datos
    if opcion == "Tamaño de muestra (población desconocida)":
        st.subheader("Tamaño de muestra cuando se desconoce el tamaño de la población")
        Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f")
        p = st.number_input("Proporción esperada (p)", value=0.500, format="%.3f")
        q = 1 - p
        d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")

        if st.button("Calcular"):
            n = (Z**2 * p * q) / (d**2)
            st.write(f"**Tamaño de muestra necesario:** {round(n)}")

    elif opcion == "Tamaño de muestra (población conocida)":
        st.subheader("Tamaño de muestra cuando se conoce el tamaño de la población")
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

    elif opcion == "Tamaño de muestra para estimación de medias (población desconocida)":
        st.subheader("Tamaño de muestra para estimación de medias (Población desconocida)")
        Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f")
        s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
        d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")

        if st.button("Calcular"):
            n = (Z**2 * s**2) / (d**2)
            st.write(f"**Tamaño de muestra necesario:** {round(n)}")

    elif opcion == "Tamaño de muestra para estimación de medias (población conocida)":
        st.subheader("Tamaño de muestra para estimación de medias (Población conocida)")
        N = st.number_input("Tamaño de la población (N)", value=1000)
        Z = st.number_input("Nivel de confianza (Z)", value=1.960, format="%.3f")
        s = st.number_input("Desviación estándar (s)", value=1.000, format="%.3f")
        d = st.number_input("Margen de error (d)", value=0.050, format="%.3f")

        if st.button("Calcular"):
            num = N * (Z**2 * s**2)
            den = (d**2 * (N - 1)) + (Z**2 * s**2)
            n = num / den
            st.write(f"**Tamaño de muestra necesario:** {round(n)}")

    elif opcion == "Ajuste por pérdidas esperadas":
        st.subheader("Ajuste por pérdidas esperadas")
        n = st.number_input("Tamaño de muestra inicial (n)", value=100)
        pe = st.number_input("Porcentaje de pérdidas esperadas (p_e, en decimal)", value=0.100, format="%.3f")

        if st.button("Calcular"):
            nc = n / (1 - pe)
            st.write(f"**Tamaño de muestra ajustado:** {round(nc)}")    
