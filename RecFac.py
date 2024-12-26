import cv2
import numpy as np
import face_recognition
import mysql.connector
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Conectar a la base de datos MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto según tu configuración
        password="R@bbit7450",  # Cambia esto según tu configuración
        database="reconocimiento_facial"
    )

# Guardar el vector facial en un archivo JSON
def guardar_vector_facial(usuario_id, vector_facial):
    filename = f"vector_facial_usuario_{usuario_id}.json"
    with open(filename, 'w') as f:
        json.dump(vector_facial.tolist(), f)  # Guardamos el vector como lista en JSON
    return filename

def guardar_usuario(nombre, correo, vector_facial_url):
    conn = conectar_mysql()
    cursor = conn.cursor()
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO usuarios (nombre, correo, fecha_registro, vector_facial_url) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nombre, correo, fecha_registro, vector_facial_url))
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return usuario_id

# Registrar acceso en la base de datos
def registrar_acceso(usuario_id, resultado_comparacion):
    conn = conectar_mysql()
    cursor = conn.cursor()
    fecha_acceso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO registros_acceso (usuario_id, fecha, resultado_comparacion) VALUES (%s, %s, %s)"
    cursor.execute(query, (usuario_id, fecha_acceso, resultado_comparacion))
    conn.commit()
    conn.close()

# Extraer el vector facial de una imagen
def obtener_vector_facial(imagen):
    # Convertir la imagen a RGB
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    # Detectar las caras en la imagen
    caras = face_recognition.face_locations(imagen_rgb)
    # Obtener los vectores faciales
    vectores = face_recognition.face_encodings(imagen_rgb, caras)
    return vectores

# Comparar dos vectores faciales
def comparar_vectores(vector1, vector2):
    # Compara dos vectores faciales usando una métrica de similitud (por ejemplo, distancia euclidiana)
    distancia = np.linalg.norm(np.array(vector1) - np.array(vector2))
    return distancia

# Función para registrar un nuevo usuario
def registrar_nuevo_usuario():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    print("Por favor, mire a la cámara para registrar su rostro.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        # Mostrar la imagen capturada
        cv2.imshow('Capturando imagen', frame)

        # Detectar la tecla 'q' para capturar la imagen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Obtener el vector facial de la imagen capturada
    vectores = obtener_vector_facial(frame)
    if len(vectores) == 0:
        print("No se detectó un rostro en la imagen.")
        return

    # Pedir los datos del usuario mediante un cuadro de diálogo
    nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
    correo = simpledialog.askstring("Correo", "Ingrese su correo electrónico:")

    if not nombre or not correo:
        messagebox.showerror("Error", "Los datos del usuario son requeridos.")
        return

    # Guardar el vector facial en un archivo JSON
    archivo_vector = guardar_vector_facial(None, vectores[0])  # Esto genera la ruta del archivo JSON

    # Guardar el usuario en la base de datos (ahora pasando también el archivo_vector como parámetro)
    usuario_id = guardar_usuario(nombre, correo, archivo_vector)

    print(f"Usuario registrado con éxito. Vector facial guardado en {archivo_vector}")
    messagebox.showinfo("Éxito", f"Usuario registrado con éxito. Vector facial guardado en {archivo_vector}")

# Función para realizar el reconocimiento facial
def reconocimiento_facial():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    print("Por favor, mire a la cámara para realizar el reconocimiento facial.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        # Mostrar la imagen capturada
        cv2.imshow('Capturando imagen', frame)

        # Detectar la tecla 'q' para capturar la imagen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Obtener el vector facial de la imagen capturada
    vectores = obtener_vector_facial(frame)
    if len(vectores) == 0:
        print("No se detectó un rostro en la imagen.")
        return

    vector_nuevo = vectores[0]

    # Comparar con los vectores faciales almacenados
    usuario_encontrado = False
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, vector_facial_url FROM usuarios")
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        usuario_id, vector_facial_url = usuario
        if vector_facial_url is None or vector_facial_url == "":
            print(f"Error: El usuario {usuario_id} no tiene una URL de vector facial válida.")
            continue  # Salta a la siguiente iteración si no hay URL válida

        with open(vector_facial_url, 'r') as f:
            vector_guardado = json.load(f)

        distancia = comparar_vectores(vector_nuevo, vector_guardado)

        # Si la distancia es pequeña, consideramos que es el mismo usuario
        if distancia < 0.6:  # Umbral de comparación
            print(f"Rostro reconocido como {usuario_id}")
            registrar_acceso(usuario_id, 1 - distancia)  # Guardar el resultado de la comparación
            usuario_encontrado = True
            break

    if not usuario_encontrado:
        print("No se pudo reconocer el rostro.")
        messagebox.showerror("Error", "No se pudo reconocer el rostro.")
    conn.close()

# Función para mostrar el menú en la interfaz gráfica
def mostrar_menu():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Sistema de Reconocimiento Facial")

    # Crear los botones de acción
    boton_registrar = tk.Button(root, text="Registrar Nuevo Usuario", command=registrar_nuevo_usuario, width=30)
    boton_registrar.pack(pady=20)

    boton_reconocer = tk.Button(root, text="Reconocimiento Facial", command=reconocimiento_facial, width=30)
    boton_reconocer.pack(pady=20)

    boton_salir = tk.Button(root, text="Salir", command=root.quit, width=30)
    boton_salir.pack(pady=20)

    # Ejecutar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    mostrar_menu()
