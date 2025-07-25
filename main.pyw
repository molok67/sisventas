from tkinter import *
from productos import abrir_ventana_productos  
from ventas import abrir_ventana_ventas
from clientes import abrir_ventana_clientes
from reportes import abrir_ventana_reportes




def abrir_ventas():
    print("Módulo de ventas (pendiente)")

def abrir_clientes():
    print("Módulo de clientes (pendiente)")

root = Tk()
root.title("Sistema de Gestión de Tienda")
root.geometry("900x600")
root.config(bg="#A6CAEE")
root.resizable(False, False)
root.config(bg="#C264DF")
 



Label(root, text="farmacias el coral",fg="blue", bg="yellow", font=("Arial", 25)).pack(pady=10)

Button(root, text="Productos", font=("Arial", 30), bg= "red", width=20, command=abrir_ventana_productos).pack(pady=5)
Button(root, text="Registrar Venta", font=("Arial", 30), bg="green", width=20, command=abrir_ventana_ventas).pack(pady=10)
Button(root, text="Gestión de Clientes", font=("Arial", 30), bg="yellow", width=20, command=abrir_ventana_clientes).pack(pady=10)
Button(root, text="Reporte de Ventas", font=("Arial", 30), width=20, bg="orange", command=abrir_ventana_reportes).pack(pady=10)
Button(root, text="Salir", font=("Arial", 30), width=20, bg="blue", command=root.quit).pack(pady=20)





root.mainloop()
