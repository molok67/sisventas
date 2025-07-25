import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

def abrir_ventana_reportes():
    ventana = Toplevel()
    ventana.title("Reporte de Ventas")
    ventana.geometry("700x500")

    # === Función para cargar ventas por fecha ===
    def buscar_ventas():
        fecha_inicio = entry_fecha_inicio.get()
        fecha_fin = entry_fecha_fin.get()

        # Validar fechas
        try:
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Las fechas deben estar en formato YYYY-MM-DD.")
            return

        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                total REAL,
                fecha TEXT
            )
        """)

        cursor.execute("""
            SELECT id, cliente, total, fecha 
            FROM ventas
            WHERE date(fecha) BETWEEN ? AND ?
            ORDER BY fecha ASC
        """, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        conexion.close()

        if ventas:
            for venta in ventas:
                tabla.insert("", END, values=venta)
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron ventas en este rango de fechas.")

    # === Función para mostrar detalles de una venta ===
    def ver_detalle():
        seleccion = tabla.focus()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona una venta para ver detalles.")
            return

        venta_id = tabla.item(seleccion)["values"][0]

        ventana_detalle = Toplevel(ventana)
        ventana_detalle.title(f"Detalle de Venta #{venta_id}")
        ventana_detalle.geometry("400x300")

        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                precio REAL
            )
        """)
        cursor.execute("""
            SELECT p.nombre, dv.cantidad, dv.precio, (dv.cantidad * dv.precio)
            FROM detalle_venta dv
            JOIN productos p ON p.id = dv.producto_id
            WHERE dv.venta_id = ?
        """, (venta_id,))
        detalles = cursor.fetchall()
        conexion.close()

        tabla_detalle = ttk.Treeview(ventana_detalle, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
        tabla_detalle.heading("Producto", text="Producto")
        tabla_detalle.heading("Cantidad", text="Cantidad")
        tabla_detalle.heading("Precio", text="Precio")
        tabla_detalle.heading("Subtotal", text="Subtotal")
        tabla_detalle.pack(fill=BOTH, expand=True, pady=10)

        for det in detalles:
            tabla_detalle.insert("", END, values=det)

    # === Widgets ===
    frame_fechas = Frame(ventana)
    frame_fechas.pack(pady=10)

    Label(frame_fechas, text="Fecha inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
    entry_fecha_inicio = Entry(frame_fechas, width=15)
    entry_fecha_inicio.grid(row=0, column=1, padx=5)

    Label(frame_fechas, text="Fecha fin (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
    entry_fecha_fin = Entry(frame_fechas, width=15)
    entry_fecha_fin.grid(row=0, column=3, padx=5)

    Button(frame_fechas, text="Buscar Ventas", command=buscar_ventas).grid(row=0, column=4, padx=10)

    # === Tabla ===
    tabla = ttk.Treeview(ventana, columns=("ID", "Cliente", "Total", "Fecha"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Total", text="Total")
    tabla.heading("Fecha", text="Fecha")
    tabla.pack(fill=BOTH, expand=True, pady=10)

    Button(ventana, text="Ver Detalle de Venta", command=ver_detalle).pack(pady=10)
