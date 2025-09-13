import streamlit as st
import pandas as pd

# ---------------- FUNCIONES DE ALGORITMOS ---------------- #
def fcfs(processes):
    tiempo = 0
    resultados = []
    for nombre, tiempo_proc, prioridad in processes:
        inicio = tiempo
        fin = inicio + tiempo_proc
        espera = inicio
        resultados.append([nombre, tiempo_proc, prioridad, inicio, fin, espera])
        tiempo = fin
    return resultados

def sjf(processes):
    lista = [[p[0], p[1], p[2]] for p in processes]  # [nombre, tiempo, prioridad]
    tiempo = 0
    resultados = []
    while lista:
        p = min(lista, key=lambda x: x[1])  # proceso con menor tiempo
        nombre, tiempo_proc, prioridad = p
        inicio = tiempo
        fin = inicio + tiempo_proc
        espera = inicio
        resultados.append([nombre, tiempo_proc, prioridad, inicio, fin, espera])
        tiempo = fin
        lista.remove(p)
    return resultados

def prioridad_alg(processes):
    lista = [[p[0], p[1], p[2]] for p in processes]  # [nombre, tiempo, prioridad]
    tiempo = 0
    resultados = []
    while lista:
        p = min(lista, key=lambda x: x[2])  # menor número = mayor prioridad
        nombre, tiempo_proc, prioridad = p
        inicio = tiempo
        fin = inicio + tiempo_proc
        espera = inicio
        resultados.append([nombre, tiempo_proc, prioridad, inicio, fin, espera])
        tiempo = fin
        lista.remove(p)
    return resultados

def round_robin(processes, quantum=2):
    pendientes = [[p[0], p[1]] for p in processes]  # [Proceso, Tiempo restante]
    tiempos_originales = {p[0]: p[1] for p in processes}
    fin_proceso = {}
    rondas = []
    ronda_num = 1
    tiempo_total = 0  # Tiempo global

    while pendientes:
        ronda_actual = []
        for p in pendientes[:]:
            nombre, tiempo_rest = p

            # 🔹 Tiempo en el que inicia esta ejecución
            ti = tiempo_total  

            # ⚡ Si es el único proceso pendiente, se ejecuta todo
            if len(pendientes) == 1:
                ejec = tiempo_rest
            else:
                ejec = min(tiempo_rest, quantum)

            tr = tiempo_rest - ejec  
            te = tiempo_total  # tiempo antes de ejecutar
            tiempo_total += ejec  # avanzar reloj

            # Guardar ejecución
            ronda_actual.append([nombre, ti, ejec, tr, te])

            # Terminado o pendiente
            if tr == 0:
                fin_proceso[nombre] = tiempo_total
                pendientes.remove(p)
            else:
                p[1] = tr

        rondas.append((ronda_num, ronda_actual))
        ronda_num += 1

    # Calcular métricas finales
    tiempos_retorno = {}
    tiempos_espera_final = {}
    for nombre in tiempos_originales:
        tat = fin_proceso[nombre]  # Tiempo de finalización
        espera = tat - tiempos_originales[nombre]  # Tiempo de espera total
        tiempos_retorno[nombre] = tat
        tiempos_espera_final[nombre] = espera

    promedio_espera = sum(tiempos_espera_final.values()) / len(tiempos_espera_final)
    promedio_retorno = sum(tiempos_retorno.values()) / len(tiempos_retorno)

    # Crear lista de DataFrames por ronda
    rondas_dfs = []
    for num, ronda in rondas:
        df = pd.DataFrame(
            ronda,
            columns=["P", "Ti", "t", "Tr", "te"]
        )
        rondas_dfs.append((num, df))

    return rondas_dfs, promedio_espera, promedio_retorno

# ---------------- INTERFAZ STREAMLIT ---------------- #
st.set_page_config(page_title="Planificación de Procesos", page_icon="⚙️", layout="wide")

st.title("⚙️ Simulador de Algoritmos de Planificación")
st.write("Ingresa los procesos con su tiempo de ejecución y prioridad. El sistema calculará automáticamente FCFS, SJF, Prioridad y Round Robin.")

st.subheader("➕ Ingresar Procesos")
num = st.number_input("Número de procesos", 1, 10, 4)

procesos = []
for i in range(num):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.text_input(f"Proceso {i+1}", f"P{i+1}")
    with col2:
        tiempo_proc = st.number_input(f"Tiempo {i+1}", 1, 50, i+2)
    with col3:
        prioridad = st.number_input(f"Prioridad {i+1}", 1, 10, 1)
    procesos.append([nombre, tiempo_proc, prioridad])

quantum = st.number_input("Quantum para Round Robin", 1, 10, 2)

if st.button("Calcular"):
    st.subheader("📊 Resultados")
    algoritmos = {
        "FCFS": fcfs,
        "SJF": sjf,
        "Prioridad": prioridad_alg
    }

    espera_promedios = {}

    # Algoritmos tradicionales
    for nombre_alg, funcion in algoritmos.items():
        st.markdown(f"### 🔹 {nombre_alg}")
        resultados = funcion(procesos)
        df = pd.DataFrame(resultados, columns=["Proceso", "Tiempo", "Prioridad", "Inicio", "Fin", "Espera"])
        st.dataframe(df, use_container_width=True)

        # Calcular tiempo de espera promedio
        espera_por_proceso = {}
        for row in resultados:
            nombre = row[0]
            espera = row[5]
            espera_por_proceso[nombre] = espera_por_proceso.get(nombre, 0) + espera
        promedio_espera = sum(espera_por_proceso.values()) / len(espera_por_proceso)
        espera_promedios[nombre_alg] = promedio_espera
        st.metric("⏳ Tiempo de espera promedio", round(promedio_espera, 2))
        st.divider()

    # Round Robin
    st.markdown("### 🔹 Round Robin")
    rondas_dfs, rr_promedio_espera, rr_promedio_retorno = round_robin(procesos, quantum)

    for num, df in rondas_dfs:
        st.markdown(f"#### Ronda {num}")
        st.dataframe(df, use_container_width=True)

    espera_promedios["Round Robin"] = rr_promedio_espera
    st.metric("⏳ Tiempo de espera promedio", round(rr_promedio_espera, 2))
    st.metric("📌 Tiempo de retorno promedio", round(rr_promedio_retorno, 2))
    st.divider()

    st.subheader("🏆 Algoritmo más óptimo")
    mejor = min(espera_promedios, key=espera_promedios.get)
    st.write(f"El algoritmo con menor tiempo de espera promedio es **{mejor}** con {round(espera_promedios[mejor],2)} unidades de tiempo.")
