import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

def abrir_ventana_clientes():
    ventana = Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("600x400")

    # === Conexión inicial ===
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            correo TEXT
        )
    """)
    conexion.commit()

    # === Funciones ===
    def cargar_clientes():
        for fila in tabla.get_children():
            tabla.delete(fila)

        cursor.execute("SELECT * FROM clientes")
        for cliente in cursor.fetchall():
            tabla.insert("", END, values=cliente)

    def agregar_cliente():
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio.")
            return

        cursor.execute("INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)", (nombre, telefono, correo))
        conexion.commit()
        cargar_clientes()
        limpiar_campos()

    def eliminar_cliente():
        seleccion = tabla.focus()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona un cliente para eliminar.")
            return

        cliente_id = tabla.item(seleccion)["values"][0]
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexion.commit()
        cargar_clientes()

    def seleccionar_cliente():
        seleccion = tabla.focus()
        if not seleccion:
            return
        datos = tabla.item(seleccion)["values"]
        entry_nombre.delete(0, END)
        entry_telefono.delete(0, END)
        entry_correo.delete(0, END)
        entry_nombre.insert(0, datos[1])
        entry_telefono.insert(0, datos[2])
        entry_correo.insert(0, datos[3])

    def modificar_cliente():
        seleccion = tabla.focus()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona un cliente para modificar.")
            return

        cliente_id = tabla.item(seleccion)["values"][0]
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()

        cursor.execute("UPDATE clientes SET nombre = ?, telefono = ?, correo = ? WHERE id = ?",
                       (nombre, telefono, correo, cliente_id))
        conexion.commit()
        cargar_clientes()
        limpiar_campos()

    def limpiar_campos():
        entry_nombre.delete(0, END)
        entry_telefono.delete(0, END)
        entry_correo.delete(0, END)

    # === Formulario ===
    frame_form = Frame(ventana)
    frame_form.pack(pady=10)

    Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    Label(frame_form, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
    entry_telefono = Entry(frame_form)
    entry_telefono.grid(row=1, column=1)

    Label(frame_form, text="Correo:").grid(row=2, column=0, padx=5, pady=5)
    entry_correo = Entry(frame_form)
    entry_correo.grid(row=2, column=1)

    frame_botones = Frame(ventana)
    frame_botones.pack()

    Button(frame_botones, text="Agregar", width=12, command=agregar_cliente).grid(row=0, column=0, padx=5, pady=5)
    Button(frame_botones, text="Modificar", width=12, command=modificar_cliente).grid(row=0, column=1, padx=5, pady=5)
    Button(frame_botones, text="Eliminar", width=12, command=eliminar_cliente).grid(row=0, column=2, padx=5, pady=5)

    # === Tabla ===
    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Teléfono", "Correo"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Teléfono", text="Teléfono")
    tabla.heading("Correo", text="Correo")
    tabla.pack(pady=10, fill=BOTH, expand=True)

    tabla.bind("<<TreeviewSelect>>", lambda e: seleccionar_cliente())

    cargar_clientes()
    ventana.mainloop()
