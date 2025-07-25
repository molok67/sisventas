import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

def abrir_ventana_ventas():
    ventana = Toplevel()
    ventana.title("Registrar Venta")
    ventana.geometry("600x500")

    # === Función para cargar productos desde la base de datos ===
    def cargar_productos():
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos

    productos_disponibles = cargar_productos()
    carrito = []

    def agregar_producto():
        seleccion = combo_producto.get()
        cantidad = entry_cantidad.get()

        if not seleccion or not cantidad.isdigit():
            messagebox.showwarning("Error", "Selecciona un producto y una cantidad válida.")
            return

        cantidad = int(cantidad)
        for id, nombre, precio in productos_disponibles:
            if nombre == seleccion:
                subtotal = precio * cantidad
                carrito.append((id, nombre, cantidad, precio, subtotal))
                tabla.insert("", END, values=(nombre, cantidad, f"${precio:.2f}", f"${subtotal:.2f}"))
                actualizar_total()
                break

    def actualizar_total():
        total = sum(item[4] for item in carrito)
        label_total.config(text=f"Total: ${total:.2f}")

    def registrar_venta():
        cliente = entry_cliente.get()
        if not cliente or not carrito:
            messagebox.showwarning("Error", "Ingresa nombre del cliente y al menos un producto.")
            return
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        total REAL,
        fecha TEXT
                 )
                     """)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ventas (cliente, total, fecha) VALUES (?, ?, ?)", (cliente, sum(i[4] for i in carrito), fecha))
       
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT, total REAL)")
        cursor.execute("INSERT INTO ventas (cliente, total) VALUES (?, ?)", (cliente, sum(i[4] for i in carrito)))
        id_venta = cursor.lastrowid

        cursor.execute("CREATE TABLE IF NOT EXISTS detalle_venta (id INTEGER PRIMARY KEY AUTOINCREMENT, venta_id INTEGER, producto_id INTEGER, cantidad INTEGER, precio REAL)")
        for item in carrito:
            cursor.execute("INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio) VALUES (?, ?, ?, ?)",
                           (id_venta, item[0], item[2], item[3]))

        conexion.commit()
        conexion.close()
        messagebox.showinfo("Venta registrada", "La venta fue registrada con éxito.")
        ventana.destroy()

    # === Widgets ===
    Label(ventana, text="Cliente:").pack(pady=5)
    entry_cliente = Entry(ventana, width=40)
    entry_cliente.pack(pady=5)

    Label(ventana, text="Producto:").pack()
    combo_producto = ttk.Combobox(ventana, values=[p[1] for p in productos_disponibles])
    combo_producto.pack()

    Label(ventana, text="Cantidad:").pack()
    entry_cantidad = Entry(ventana)
    entry_cantidad.pack(pady=5)

    Button(ventana, text="Agregar al carrito", command=agregar_producto).pack(pady=5)

    # === Tabla ===
    tabla = ttk.Treeview(ventana, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
    tabla.heading("Producto", text="Producto")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Subtotal", text="Subtotal")
    tabla.pack(pady=10, fill=BOTH, expand=True)

    label_total = Label(ventana, text="Total: $0.00", font=("Arial", 12, "bold"))
    label_total.pack(pady=10)

    Button(ventana, text="Registrar Venta", command=registrar_venta).pack(pady=10)
