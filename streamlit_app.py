import re
import tkinter as tk
from tkinter import ttk, scrolledtext

# =========================
# TEMAS
# =========================
tema_oscuro = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "editor": "#252526"
}

tema_claro = {
    "bg": "#ffffff",
    "fg": "#000000",
    "editor": "#f5f5f5"
}

tema_actual = tema_oscuro

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
# TOKENS
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
# ANALIZADOR
# =========================
def analizar(codigo):
    tokens = []
    errores = []
    lineas_error = set()
    contador = 1

    lineas = codigo.split("\n")

    for num_linea, linea in enumerate(lineas, start=1):
        linea = re.sub(r'//.*', '', linea)
        pos = 0

        while pos < len(linea):

            if re.match(r'\s', linea[pos]):
                pos += 1
                continue

            match = None

            for tipo, regex in tokens_regex:
                patron = re.compile(regex)
                match = patron.match(linea, pos)

                if match:
                    lexema = match.group(0)

                    if tipo == "T_ID" and lexema in reservadas:
                        tipo = reservadas[lexema]

                    tokens.append((contador, lexema, tipo))
                    contador += 1
                    pos = match.end(0)
                    break

            if not match:
                errores.append((
                    len(errores)+1,
                    f"Línea {num_linea}",
                    f"Símbolo inválido: '{linea[pos]}'",
                    "Verifica el carácter"
                ))

                lineas_error.add(num_linea)
                pos += 1

    return tokens, errores, lineas_error

# =========================
# FUNCIONES UI
# =========================
def ejecutar():
    codigo = txt_codigo.get("1.0", tk.END)
    tokens, errores, lineas_error = analizar(codigo)

    # Limpiar tablas
    for row in tabla_tokens.get_children():
        tabla_tokens.delete(row)

    for row in tabla_errores.get_children():
        tabla_errores.delete(row)

    # Insertar tokens
    for t in tokens:
        tabla_tokens.insert("", tk.END, values=t)

    # Insertar errores
    for e in errores:
        tabla_errores.insert("", tk.END, values=e)

    # Resaltar errores
    resaltar_errores(lineas_error)


def limpiar():
    txt_codigo.delete("1.0", tk.END)

    for row in tabla_tokens.get_children():
        tabla_tokens.delete(row)

    for row in tabla_errores.get_children():
        tabla_errores.delete(row)


def cambiar_tema():
    global tema_actual
    tema_actual = tema_claro if tema_actual == tema_oscuro else tema_oscuro
    aplicar_tema()


# =========================
# RESALTADO DE ERRORES
# =========================
def resaltar_errores(lineas_error):
    txt_codigo.tag_remove("error", "1.0", tk.END)

    for linea in lineas_error:
        inicio = f"{linea}.0"
        fin = f"{linea}.end"
        txt_codigo.tag_add("error", inicio, fin)

    txt_codigo.tag_config("error", background="red", foreground="white")

    ventana.after(5000, limpiar_resaltado)


def limpiar_resaltado():
    txt_codigo.tag_remove("error", "1.0", tk.END)


# =========================
# TEMA
# =========================
def aplicar_tema():
    ventana.configure(bg=tema_actual["bg"])

    # Editor
    txt_codigo.configure(
        bg=tema_actual["editor"],
        fg=tema_actual["fg"],
        insertbackground=tema_actual["fg"]
    )

    # Labels
    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=tema_actual["bg"], fg=tema_actual["fg"])

    # Botones
    for widget in toolbar.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(
                bg=tema_actual["editor"],
                fg=tema_actual["fg"],
                activebackground=tema_actual["bg"],
                activeforeground=tema_actual["fg"]
            )

    # Tablas
    style.configure("Treeview",
        background=tema_actual["editor"],
        foreground=tema_actual["fg"],
        fieldbackground=tema_actual["editor"]
    )

    style.configure("Treeview.Heading",
        background=tema_actual["bg"],
        foreground=tema_actual["fg"]
    )


# =========================
# INTERFAZ
# =========================
ventana = tk.Tk()
ventana.title("SimplePy IDE")
ventana.geometry("1000x650")

# Estilo
style = ttk.Style()
style.theme_use("clam")

# Toolbar
toolbar = tk.Frame(ventana)
toolbar.pack(fill="x")

tk.Button(toolbar, text="▶ Traducir", command=ejecutar).pack(side="left", padx=5)
tk.Button(toolbar, text="🌙/☀ Tema", command=cambiar_tema).pack(side="left", padx=5)
tk.Button(toolbar, text="🧹 Limpiar", command=limpiar).pack(side="left", padx=5)

# Editor
tk.Label(ventana, text="Código SimplePy").pack()

txt_codigo = scrolledtext.ScrolledText(ventana, height=10)
txt_codigo.pack(fill="both", expand=True)

# Tabla tokens
tk.Label(ventana, text="Tabla de Símbolos").pack()

tabla_tokens = ttk.Treeview(ventana, columns=("N°", "Lexema", "Token"), show="headings")
tabla_tokens.heading("N°", text="N°")
tabla_tokens.heading("Lexema", text="Lexema")
tabla_tokens.heading("Token", text="Token")
tabla_tokens.pack(fill="both", expand=True)

# Tabla errores
tk.Label(ventana, text="Errores Léxicos").pack()

tabla_errores = ttk.Treeview(
    ventana,
    columns=("N°", "Descripción", "Detalle", "Sugerencia"),
    show="headings"
)

tabla_errores.heading("N°", text="N°")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.heading("Detalle", text="Detalle")
tabla_errores.heading("Sugerencia", text="Sugerencia")
tabla_errores.pack(fill="both", expand=True)

# Aplicar tema inicial
aplicar_tema()

ventana.mainloop()