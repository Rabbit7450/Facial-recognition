import cv2
import numpy as np
import face_recognition
import pymongo
import json
from datetime import datetime
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Configuración de la clave de cifrado
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Conexión a MongoDB
def conectar_mongodb():
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["reconocimiento_facial"]
    return db

# Guardar el vector facial cifrado en MongoDB
def guardar_vector_facial_en_mongo(usuario_id, vector_facial):
    db = conectar_mongodb()
    coleccion = db["usuarios"]

    # Cifrar el vector facial
    vector_cifrado = cipher_suite.encrypt(json.dumps(vector_facial.tolist()).encode())

    documento = {
        "usuario_id": usuario_id,
        "vector_facial": vector_cifrado,
        "fecha_registro": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    coleccion.insert_one(documento)
    print(f"Vector facial de usuario {usuario_id} guardado en MongoDB.")

# Guardar usuario en MongoDB
def guardar_usuario_en_mongo(nombre, correo):
    db = conectar_mongodb()
    coleccion = db["usuarios"]

    documento = {
        "nombre": nombre,
        "correo": correo,
        "fecha_registro": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    usuario = coleccion.insert_one(documento)
    return usuario.inserted_id

# Obtener el vector facial de una imagen
def obtener_vector_facial(imagen):
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    caras = face_recognition.face_locations(imagen_rgb)
    vectores = face_recognition.face_encodings(imagen_rgb, caras)
    return vectores

# Comparar dos vectores faciales
def comparar_vectores(vector1, vector2):
    distancia = np.linalg.norm(np.array(vector1) - np.array(vector2))
    return distancia

# Registrar acceso en MongoDB
def registrar_acceso(usuario_id, resultado_comparacion):
    db = conectar_mongodb()
    coleccion = db["accesos"]

    acceso = {
        "usuario_id": usuario_id,
        "fecha_acceso": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "resultado_comparacion": resultado_comparacion
    }

    coleccion.insert_one(acceso)
    print(f"Acceso registrado para el usuario {usuario_id} con similitud {resultado_comparacion}.")

# Función para registrar un nuevo usuario
def registrar_nuevo_usuario():
    print("Iniciando el proceso de registro...")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: No se puede abrir la camara.")
        return 
    print("Por favor, mire a la cámara para registrar su rostro.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        cv2.imshow('Capturando imagen', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    vectores = obtener_vector_facial(frame)
    if len(vectores) == 0:
        print("No se detectó un rostro en la imagen.")
        return

    nombre = input("Ingrese su nombre: ")
    correo = input("Ingrese su correo electrónico: ")

    usuario_id = guardar_usuario_en_mongo(nombre, correo)
    guardar_vector_facial_en_mongo(usuario_id, vectores[0])

    print(f"Usuario registrado con éxito en MongoDB. ID: {usuario_id}")

# Función para realizar el reconocimiento facial en tiempo real
def reconocimiento_facial():
    print("Iniciando el reconocimiento facial...")
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        cv2.imshow('Reconocimiento Facial', frame)

        vectores = obtener_vector_facial(frame)
        if len(vectores) == 0:
            print("No se detectó un rostro en la imagen.")
            continue

        vector_nuevo = vectores[0]

        db = conectar_mongodb()
        coleccion = db["usuarios"]
        usuarios = coleccion.find()

        usuario_encontrado = False
        for usuario in usuarios:
            vector_facial_cifrado = usuario["vector_facial"]
            vector_facial_descifrado = cipher_suite.decrypt(vector_facial_cifrado).decode()
            vector_facial_descifrado = json.loads(vector_facial_descifrado)

            distancia = comparar_vectores(vector_nuevo, vector_facial_descifrado)
            if distancia < 0.6:
                print(f"Rostro reconocido como {usuario['nombre']}. Similitud: {1 - distancia:.2f}")
                registrar_acceso(usuario["_id"], 1 - distancia)
                usuario_encontrado = True
                break

        if not usuario_encontrado:
            print("No se pudo reconocer el rostro.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Interfaz gráfica básica con Tkinter
def interfaz_usuario():
    def registrar_usuario_gui():
        registrar_nuevo_usuario()
        messagebox.showinfo("Registro completado", "Usuario registrado exitosamente.")

    def iniciar_reconocimiento_gui():
        reconocimiento_facial()

    root = tk.Tk()
    root.title("Aplicación de Reconocimiento Facial")

    tk.Button(root, text="Registrar Nuevo Usuario", command=registrar_usuario_gui).pack(pady=10)
    tk.Button(root, text="Iniciar Reconocimiento Facial", command=iniciar_reconocimiento_gui).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    interfaz_usuario()