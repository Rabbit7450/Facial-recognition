import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Función para conectar a la base de datos MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto según tu configuración
        password="R@bbit7450",  # Cambia esto según tu configuración
        database="reconocimiento_facial"
    )

# Función para mostrar la información del usuario
def mostrar_informacion_usuario(usuario_id):
    # Conectar a la base de datos
    conn = conectar_mysql()
    cursor = conn.cursor()
    
    # Realizar la consulta para obtener la información del usuario
    query = "SELECT nombre, correo, fecha_registro FROM usuarios WHERE id = %s"
    cursor.execute(query, (usuario_id,))
    usuario = cursor.fetchone()
    
    # Si el usuario no existe, mostrar un mensaje de error
    if not usuario:
        messagebox.showerror("Error", "No se encontró información del usuario.")
        conn.close()
        return
    
    nombre, correo, fecha_registro = usuario
    conn.close()

    # Crear una nueva ventana para mostrar la información
    ventana_info = tk.Toplevel()
    ventana_info.title(f"Información de {nombre}")
    ventana_info.geometry("300x200")

    # Etiquetas con la información del usuario
    etiqueta_nombre = tk.Label(ventana_info, text=f"Nombre: {nombre}")
    etiqueta_nombre.pack(pady=10)
    
    etiqueta_correo = tk.Label(ventana_info, text=f"Correo: {correo}")
    etiqueta_correo.pack(pady=10)
    
    etiqueta_fecha = tk.Label(ventana_info, text=f"Fecha de Registro: {fecha_registro}")
    etiqueta_fecha.pack(pady=10)

    # Botón para cerrar la ventana
    boton_cerrar = tk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy)
    boton_cerrar.pack(pady=20)

    ventana_info.mainloop()
