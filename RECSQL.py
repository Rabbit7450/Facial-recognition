import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import mysql.connector
import json
import numpy as np
import face_recognition
import os
from datetime import datetime
import bcrypt  # Importamos bcrypt para cifrar contraseñas
from PIL import Image, ImageTk

def s_d_g(titulo, mensaje):
    # Crear una ventana nueva
    ventana = tk.Toplevel()
    ventana.title(titulo)

    # Hacer la ventana más grande
    ventana.geometry("400x200")  # Tamaño más grande, ajusta según lo necesites

        # Personalizar fondo de la ventana
    ventana.configure(bg="#f4f4f9")

    # Cargar la imagen de fondo
    fondo_imagen = Image.open("C:/Users/Adalit Ticona/Downloads/fond.jpg")  # Pon la ruta a tu imagen aquí
    fondo_imagen = fondo_imagen.resize((600, 400))  # Redimensionamos la imagen al tamaño de la ventana
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen)

    # Etiqueta con el mensaje
    etiqueta = tk.Label(ventana, text=mensaje, font=("Arial", 14))
    etiqueta.pack(pady=20)

    # Campo de entrada para el texto
    entrada = tk.Entry(ventana, font=("Arial", 14), width=30)
    entrada.pack(pady=10)

    # Variable para almacenar el resultado
    resultado = None

    # Función para cuando el usuario haga clic en "Aceptar"
    def aceptar():
        nonlocal resultado
        resultado = entrada.get()
        ventana.destroy()

    # Botón para aceptar
    boton_aceptar = tk.Button(ventana, text="Aceptar", font=("Arial", 14), command=aceptar)
    boton_aceptar.pack(pady=10)

    # Hacer que la ventana sea modal (bloqueante hasta que se cierre)
    ventana.wait_window()

    return resultado


# Conectar a la base de datos MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto según tu configuración
        password="R@bbit7450",  # Cambia esto según tu configuración
        database="reconocimiento_facial"
    )

# Verificar si el usuario ya existe en la base de datos
def verificar_usuario_existente(nombre, correo):
    conn = conectar_mysql()
    cursor = conn.cursor()
    query = "SELECT id FROM usuarios WHERE correo = %s OR nombre_completo = %s"
    cursor.execute(query, (correo, nombre))
    resultado = cursor.fetchone()  # Si existe un usuario, fetchone devuelve los datos
    conn.close()
    return resultado  # Si hay resultados, el usuario ya existe

def guardar_vector_facial(vector_facial):
    # Definir la carpeta y asegurarse de que exista
    carpeta = 'vectores_faciales'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Definir el nombre del archivo JSON
    usuario_id = int(datetime.timestamp(datetime.now()))  # Crear un ID único para el archivo
    filename = os.path.join(carpeta, f"vector_facial_usuario_{usuario_id}.json")
    
    # Guardar el vector como lista en JSON
    with open(filename, 'w') as f:
        json.dump(vector_facial.tolist(), f)
    
    return filename  # Devolver la URL del archivo generado

# Función para registrar un nuevo usuario
def registrar_nuevo_usuario():
    # Capturar los datos del nuevo usuario
    nombre_completo = s_d_g("Registrar Usuario", "Ingrese su nombre completo:")
    if not nombre_completo:
        return

    correo = s_d_g("Registrar Usuario", "Ingrese su correo electrónico:")
    if not correo:
        return

    confirmar_correo = s_d_g("Registrar Usuario", "Confirme su correo electrónico:")
    if correo != confirmar_correo:
        messagebox.showerror("Error", "Los correos electrónicos no coinciden.")
        return

    fecha_nacimiento = s_d_g("Registrar Usuario", "Ingrese su fecha de nacimiento (YYYY-MM-DD):")
    if not fecha_nacimiento:
        return

    genero = s_d_g("Registrar Usuario", "Ingrese su género:")
    if not genero:
        return

    telefono = s_d_g("Registrar Usuario", "Ingrese su número de teléfono:")
    if not telefono:
        return

    direccion = s_d_g("Registrar Usuario", "Ingrese su dirección:")
    if not direccion:
        return

    ciudad = s_d_g("Registrar Usuario", "Ingrese su ciudad:")
    if not ciudad:
        return

    pais = s_d_g("Registrar Usuario", "Ingrese su país:")
    if not pais:
        return

    cargo = s_d_g("Registrar Usuario", "Ingrese su cargo:")
    if not cargo:
        return

    areas_especializacion = s_d_g("Registrar Usuario", "Ingrese sus áreas de especialización:")
    if not areas_especializacion:
        return

    objetivo_meta = s_d_g("Registrar Usuario", "Ingrese su objetivo o meta profesional:")
    if not objetivo_meta:
        return

    contrasena = simpledialog.askstring("Registrar Usuario", "Ingrese una contraseña:", show="*")
    if not contrasena:
        return

    confirmar_contrasena = simpledialog.askstring("Registrar Usuario", "Confirme su contraseña:", show="*")
    if contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    # Verificar si el usuario ya existe
    if verificar_usuario_existente(nombre_completo, correo):
        messagebox.showerror("Error", "Ya existe un usuario con ese nombre o correo electrónico.")
        return

    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Captura de rostro", "Por favor, mire a la cámara para registrar su rostro.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Error al capturar la imagen.")
            break

        cv2.imshow('Capturando imagen', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    vectores = obtener_vector_facial(frame)
    if len(vectores) == 0:
        messagebox.showerror("Error", "No se detectó un rostro en la imagen.")
        return

    # Guardar el nuevo usuario en la base de datos
    usuario_id = guardar_usuario(
        nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, 
        areas_especializacion, objetivo_meta, contrasena, None  
    )

    if usuario_id:
        # Ahora que tenemos el usuario_id, podemos guardar el vector facial
        archivo_vector = guardar_vector_facial(usuario_id, vectores[0])  # Guardamos el vector con el usuario_id real

        # Actualizamos la base de datos con la URL del archivo JSON
        conn = conectar_mysql()
        cursor = conn.cursor()
        query = "UPDATE usuarios SET vector_facial_url = %s WHERE id = %s"
        cursor.execute(query, (archivo_vector, usuario_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Usuario registrado con éxito. Vector facial guardado en {archivo_vector}")
    else:
        messagebox.showerror("Error", "No se pudo registrar el usuario.")
# Función para guardar el usuario en la base de datos
def guardar_usuario(nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, 
                    areas_especializacion, objetivo_meta, contrasena, vector_facial_url):
    # Cifrar la contraseña
    hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    # Conectar a la base de datos y registrar el nuevo usuario
    conn = conectar_mysql()
    cursor = conn.cursor()
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Consultar el INSERT para los nuevos campos
    query = """INSERT INTO usuarios (nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, 
               pais, cargo, areas_especializacion, objetivo_meta, contrasena, fecha_registro, vector_facial_url)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    cursor.execute(query, (nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, 
                           cargo, areas_especializacion, objetivo_meta, hashed_contrasena, fecha_registro, vector_facial_url))
    conn.commit()
    usuario_id = cursor.lastrowid  # Obtén el ID generado para el nuevo usuario
    conn.close()
    return usuario_id

# Extraer el vector facial de una imagen
def obtener_vector_facial(imagen):
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    caras = face_recognition.face_locations(imagen_rgb)
    vectores = face_recognition.face_encodings(imagen_rgb, caras)
    return vectores

# Función para comparar dos vectores faciales
def comparar_vectores(vector1, vector2):
    distancia = np.linalg.norm(np.array(vector1) - np.array(vector2))
    return distancia

# Crear la carpeta para almacenar los vectores faciales, si no existe
if not os.path.exists('vectores_faciales'):
    os.makedirs('vectores_faciales')

# Guardar el vector facial en un archivo JSON
def guardar_vector_facial(usuario_id, vector_facial):
    # Definir la carpeta y asegurarse de que exista
    carpeta = 'vectores_faciales'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Definir el nombre del archivo JSON
    filename = os.path.join(carpeta, f"vector_facial_usuario_{usuario_id}.json")
    
    # Guardar el vector como lista en JSON
    with open(filename, 'w') as f:
        json.dump(vector_facial.tolist(), f)
    
    return filename

# Función para realizar el reconocimiento facial (comparación de vectores faciales)
def reconocimiento_facial():
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Reconocimiento Facial", "Por favor, mire a la cámara para realizar el reconocimiento facial.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Error al capturar la imagen.")
            break

        cv2.imshow('Capturando imagen', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    vectores = obtener_vector_facial(frame)
    if len(vectores) == 0:
        messagebox.showerror("Error", "No se detectó un rostro en la imagen.")
        return

    vector_nuevo = vectores[0]
    usuario_encontrado = False
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, areas_especializacion, objetivo_meta, vector_facial_url FROM usuarios")
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        usuario_id, nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, areas_especializacion, objetivo_meta, vector_facial_url = usuario
        if vector_facial_url is None or not os.path.exists(vector_facial_url):
            continue

        # Cargar el vector facial desde el archivo JSON
        with open(vector_facial_url, 'r') as f:
            vector_guardado = json.load(f)

        # Comparar los vectores faciales
        distancia = comparar_vectores(vector_nuevo, vector_guardado)

        if distancia < 0.6:
            # Mostrar los datos del usuario reconocido
            datos_usuario = (
                f"ID: {usuario_id}\n"
                f"Nombre: {nombre_completo}\n"
                f"Correo: {correo}\n"
                f"Fecha de nacimiento: {fecha_nacimiento}\n"
                f"Género: {genero}\n"
                f"Teléfono: {telefono}\n"
                f"Dirección: {direccion}\n"
                f"Ciudad: {ciudad}\n"
                f"País: {pais}\n"
                f"Cargo: {cargo}\n"
                f"Áreas de especialización: {areas_especializacion}\n"
                f"Objetivo/Meta profesional: {objetivo_meta}"
            )
            messagebox.showinfo("Rostro Reconocido", f"Rostro reconocido como:\n{datos_usuario}")
            usuario_encontrado = True
            break

    if not usuario_encontrado:
        messagebox.showerror("Error", "No se pudo reconocer el rostro.")
    conn.close()
# Función para editar los datos del usuario
def editar_datos_usuario():
    # Solicitar el correo o ID del usuario para buscar en la base de datos
    correo = s_d_g("Editar Usuario", "Ingrese el correo electrónico del usuario a editar:")
    if not correo:
        return

    # Conectar a la base de datos y buscar al usuario
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, areas_especializacion, objetivo_meta FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()

    if not usuario:
        messagebox.showerror("Error", "Usuario no encontrado.")
        conn.close()
        return

    # Mostrar los datos actuales en cuadros de entrada para que el usuario los pueda modificar
    usuario_id, nombre_completo, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais, cargo, areas_especializacion, objetivo_meta = usuario

    # Crear ventana de edición
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Datos del Usuario")

    # Hacer la ventana más grande
    ventana_edicion.geometry("600x600") 
    # Estilo de la fuente para las etiquetas y campos
    font_label = ("Arial", 14)
    font_entry = ("Arial", 12)

     # Cargar la imagen de fondo
    fondo_imagen = Image.open("C:/Users/Adalit Ticona/Downloads/fond.jpg")  # Pon la ruta a tu imagen aquí
    fondo_imagen = fondo_imagen.resize((600, 600))  # Redimensionamos la imagen al tamaño de la ventana
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen)

        # Crear un Label para mostrar la imagen de fondo
    label_fondo = tk.Label(ventana_edicion, image=fondo_imagen_tk)
    label_fondo.place(relwidth=1, relheight=1)  # Hace que ocupe toda la ventana

    # Crear un marco para los campos de entrada y botones
    frame = tk.Frame(ventana_edicion)
    frame.pack(padx=20, pady=20)

    # Campos de entrada para los datos del usuario
    tk.Label(frame, text="Nombre Completo:", font=font_label).grid(row=0, column=0, pady=10, sticky="w")
    campo_nombre = tk.Entry(frame, font=font_entry, width=40)
    campo_nombre.insert(0, nombre_completo)
    campo_nombre.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Fecha de Nacimiento:", font=font_label).grid(row=1, column=0, pady=10, sticky="w")
    campo_fecha_nacimiento = tk.Entry(frame, font=font_entry, width=40)
    campo_fecha_nacimiento.insert(0, fecha_nacimiento)
    campo_fecha_nacimiento.grid(row=1, column=1, pady=10)

    tk.Label(frame, text="Género:", font=font_label).grid(row=2, column=0, pady=10, sticky="w")
    campo_genero = tk.Entry(frame, font=font_entry, width=40)
    campo_genero.insert(0, genero)
    campo_genero.grid(row=2, column=1, pady=10)

    tk.Label(frame, text="Teléfono:", font=font_label).grid(row=3, column=0, pady=10, sticky="w")
    campo_telefono = tk.Entry(frame, font=font_entry, width=40)
    campo_telefono.insert(0, telefono)
    campo_telefono.grid(row=3, column=1, pady=10)

    tk.Label(frame, text="Dirección:", font=font_label).grid(row=4, column=0, pady=10, sticky="w")
    campo_direccion = tk.Entry(frame, font=font_entry, width=40)
    campo_direccion.insert(0, direccion)
    campo_direccion.grid(row=4, column=1, pady=10)

    tk.Label(frame, text="Ciudad:", font=font_label).grid(row=5, column=0, pady=10, sticky="w")
    campo_ciudad = tk.Entry(frame, font=font_entry, width=40)
    campo_ciudad.insert(0, ciudad)
    campo_ciudad.grid(row=5, column=1, pady=10)

    tk.Label(frame, text="País:", font=font_label).grid(row=6, column=0, pady=10, sticky="w")
    campo_pais = tk.Entry(frame, font=font_entry, width=40)
    campo_pais.insert(0, pais)
    campo_pais.grid(row=6, column=1, pady=10)

    tk.Label(frame, text="Cargo:", font=font_label).grid(row=7, column=0, pady=10, sticky="w")
    campo_cargo = tk.Entry(frame, font=font_entry, width=40)
    campo_cargo.insert(0, cargo)
    campo_cargo.grid(row=7, column=1, pady=10)

    tk.Label(frame, text="Áreas de Especialización:", font=font_label).grid(row=8, column=0, pady=10, sticky="w")
    campo_areas_especializacion = tk.Entry(frame, font=font_entry, width=40)
    campo_areas_especializacion.insert(0, areas_especializacion)
    campo_areas_especializacion.grid(row=8, column=1, pady=10)

    tk.Label(frame, text="Objetivo o Meta Profesional:", font=font_label).grid(row=9, column=0, pady=10, sticky="w")
    campo_objetivo_meta = tk.Entry(frame, font=font_entry, width=40)
    campo_objetivo_meta.insert(0, objetivo_meta)
    campo_objetivo_meta.grid(row=9, column=1, pady=10)

    # Botón para guardar los cambios
    def guardar_cambios():
        # Obtener los nuevos datos
        nuevo_nombre = campo_nombre.get()
        nueva_fecha_nacimiento = campo_fecha_nacimiento.get()
        nuevo_genero = campo_genero.get()
        nuevo_telefono = campo_telefono.get()
        nueva_direccion = campo_direccion.get()
        nueva_ciudad = campo_ciudad.get()
        nuevo_pais = campo_pais.get()
        nuevo_cargo = campo_cargo.get()
        nuevas_areas_especializacion = campo_areas_especializacion.get()
        nuevo_objetivo_meta = campo_objetivo_meta.get()
        
        # Actualizar los datos en la base de datos
        query = """UPDATE usuarios
                   SET nombre_completo = %s, fecha_nacimiento = %s, genero = %s, telefono = %s, direccion = %s,
                       ciudad = %s, pais = %s, cargo = %s, areas_especializacion = %s, objetivo_meta = %s
                   WHERE id = %s"""
        cursor.execute(query, (nuevo_nombre, nueva_fecha_nacimiento, nuevo_genero, nuevo_telefono, nueva_direccion,
                               nueva_ciudad, nuevo_pais, nuevo_cargo, nuevas_areas_especializacion, nuevo_objetivo_meta, usuario_id))
        conn.commit()
        conn.close()
        ventana_edicion.destroy()
        messagebox.showinfo("Éxito", "Datos del usuario actualizados con éxito.")

    # Botón para guardar los cambios
    boton_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios)
    boton_guardar.pack(pady=20)

    ventana_edicion.mainloop()

# Función para abrir la ventana principal
def iniciar_gui():
    ventana = tk.Tk()
    ventana.title("Reconocimiento Facial")
    
    # Hacer la ventana más grande
    ventana.geometry("600x400")  # Ajusta el tamaño de la ventana según lo necesites

    # Personalizar fondo de la ventana
    ventana.configure(bg="#60b26c")

    # Cargar la imagen de fondo
    fondo_imagen = Image.open("C:/Users/Adalit Ticona/Downloads/fond.jpg")  # Pon la ruta a tu imagen aquí
    fondo_imagen = fondo_imagen.resize((600, 400))  # Redimensionamos la imagen al tamaño de la ventana
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen)

        # Crear un Label para mostrar la imagen de fondo
    label_fondo = tk.Label(ventana, image=fondo_imagen_tk)
    label_fondo.place(relwidth=1, relheight=1)  # Hace que ocupe toda la ventana

        # Título en la parte superior sin fondo blanco
    titulo = tk.Label(ventana, text="Sistema de Reconocimiento Facial",bg="cyan", font=("Arial", 20, "bold"), fg="#333")
    titulo.grid(row=0, column=0, columnspan=2, pady=30)

    # Crear un marco para los botones
    frame_botonera = tk.Frame(ventana, bg="#60b26c")
    frame_botonera.grid(row=1, column=0, columnspan=2, pady=20)

    # Estilo para los botones
    style = {
        'font': ("Arial", 12, "bold"),
        'fg': 'white',
        'width': 20,
        'height': 2,
        'bd': 0,  # Sin borde adicional
        'highlightthickness': 0,  # Eliminar borde adicional
        'relief': 'flat',  # Usar un solo relief aquí
        'padx': 10,
        'pady': 10,
        'bg': '#60b26c',  # Color de fondo para el botón
        'activebackground': '#60b26c'  # Fondo del botón cuando se presiona
    }

    # Botón para registrar un nuevo usuario con fondo redondeado
    boton_registrar = tk.Button(frame_botonera, text="Registrar Nuevo Usuario", command=registrar_nuevo_usuario, **style)
    boton_registrar.grid(row=0, column=0, padx=20, pady=10)

    # Estilo para el botón "Reconocer Usuario"
    style['bg'] = '#60b26c'
    style['activebackground'] = '#60b26c'

    # Botón para reconocer usuario con fondo redondeado
    boton_reconocer = tk.Button(frame_botonera, text="Reconocer Usuario", command=reconocimiento_facial, **style)
    boton_reconocer.grid(row=0, column=1, padx=20, pady=10)

    # Estilo para el botón "Editar Datos de Usuario"
    style['bg'] = '#60b26c'
    style['activebackground'] = '#60b26c'

    # Botón para editar los datos de un usuario con fondo redondeado
    boton_editar = tk.Button(frame_botonera, text="Editar Datos de Usuario", command=editar_datos_usuario, **style)
    boton_editar.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
    
    # Iniciar el bucle principal de la interfaz
    ventana.mainloop()

# Llamar a la función para iniciar la interfaz
iniciar_gui()