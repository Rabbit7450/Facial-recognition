import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk  # Importamos la librería PIL para manejar imágenes

# Función que ejecutará el script QR.py cuando se haga clic en el botón
def ejecutar_generar_qr():
    try:
        # Ejecuta el script QR.py
        subprocess.run(["python", "QR.py"])  # Asegúrate de que la ruta al archivo sea correcta
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el script QR.py: {e}")

# Función que ejecutará el script RECSQL.py cuando se haga clic en el botón
def ejecutar_reconocimiento_facial():
    try:
        # Ejecuta el script RECSQL.py
        subprocess.run(["python", "RECSQL.py"])  # Asegúrate de que la ruta al archivo sea correcta
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el script: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generación de QR")
ventana.geometry("500x300")

# Cargar la imagen de fondo (asegúrate de usar la ruta correcta a tu imagen)
fondo_imagen = Image.open("C:/Users/Adalit Ticona/Desktop/fondo.jpg")  # Aquí pones la ruta a la imagen local
fondo_imagen = fondo_imagen.resize((500, 300), Image.Resampling.LANCZOS)  # Redimensionar la imagen para ajustarla
fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen)

# Usar un Label con la imagen de fondo
fondo_label = tk.Label(ventana, image=fondo_imagen_tk)
fondo_label.place(relwidth=1, relheight=1)

# Crear un botón para ejecutar el reconocimiento facial
boton_reconocimiento = ttk.Button(ventana, text="Reconocimiento Facial", command=ejecutar_reconocimiento_facial, width=20, style="TButton")
boton_reconocimiento.pack(pady=30)

# Crear un botón para generar el QR
boton_qr = ttk.Button(ventana, text="Generar QR", command=ejecutar_generar_qr, width=20, style="TButton")
boton_qr.pack(pady=10)

# Estilo de los botones
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#3E7F7F", font=("Arial", 12, "bold"), width=20)

# Ejecutar la ventana
ventana.mainloop()
