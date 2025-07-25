import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

modo_modificacion = [False, None]


def crear_tabla():
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def agregar_producto(nombre, precio):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conexion.commit()
    conexion.close()

def actualizar_producto(id_producto, nombre, precio):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (nombre, precio, id_producto))
    conexion.commit()
    conexion.close()

def eliminar_producto(id_producto):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()

def abrir_ventana_productos():
    crear_tabla()
    ventana = Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("400x400")

    def cargar_productos():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        for row in cursor.fetchall():
            tabla.insert("", END, values=row)
        conexion.close()

    def guardar_producto():
        nombre = entry_nombre.get()
        try:
            precio = float(entry_precio.get())
            if modo_modificacion[0]:
                actualizar_producto(modo_modificacion[1], nombre, precio)
                modo_modificacion[0] = False
                modo_modificacion[1] = None
                btn_agregar.config(text="Agregar")
            else:
                agregar_producto(nombre, precio)
            entry_nombre.delete(0, END)
            entry_precio.delete(0, END)
            cargar_productos()
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")

    def eliminar_seleccionado():
        seleccionado = tabla.selection()
        if seleccionado:
            item = tabla.item(seleccionado)
            id_producto = item['values'][0]
            eliminar_producto(id_producto)
            cargar_productos()
        else:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar")

    def modificar_seleccionado():
        seleccionado = tabla.selection()
        if seleccionado:
            item = tabla.item(seleccionado)
            id_producto, nombre, precio = item['values']
            entry_nombre.delete(0, END)
            entry_precio.delete(0, END)
            entry_nombre.insert(0, nombre)
            entry_precio.insert(0, str(precio))
            modo_modificacion[0] = True
            modo_modificacion[1] = id_producto
            btn_agregar.config(text="Guardar cambios")
        else:
            messagebox.showwarning("Atención", "Selecciona un producto para modificar")

    Label(ventana, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = Entry(ventana)
    entry_nombre.grid(row=0, column=1)

    Label(ventana, text="Precio").grid(row=1, column=0, padx=5, pady=5)
    entry_precio = Entry(ventana)
    entry_precio.grid(row=1, column=1)

    btn_agregar = Button(ventana, text="Agregar", command=guardar_producto)
    btn_agregar.grid(row=2, column=0, columnspan=2, pady=5)

    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio", text="Precio")
    tabla.column("ID", width=30)
    tabla.column("Nombre", width=150)
    tabla.column("Precio", width=100)
    tabla.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    Button(ventana, text="Modificar", command=modificar_seleccionado).grid(row=4, column=0, padx=5, pady=5)
    Button(ventana, text="Eliminar", command=eliminar_seleccionado).grid(row=4, column=1, padx=5, pady=5)

    cargar_productos()
