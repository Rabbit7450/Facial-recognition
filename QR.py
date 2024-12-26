import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import uuid
import os

class QRGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Generador de Códigos QR")
        master.geometry("600x800")  # Aumenté el tamaño para acomodar más campos

        # Variables para almacenar los datos
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.confirmar_correo_var = tk.StringVar()
        self.fecha_nacimiento_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()
        self.pais_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.areas_especializacion_var = tk.StringVar()
        self.objetivo_meta_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.confirmar_contrasena_var = tk.StringVar()

        # Crear y colocar widgets
        self.create_widgets(master)

        # Imagen de fondo (se inicializa como None)
        self.fondo_imagen = None

    def create_widgets(self, master):
        # Crear un Canvas para colocar la imagen de fondo
        self.canvas = tk.Canvas(master, width=600, height=800)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=16, sticky="nsew")

        # Label y campos de texto para los datos
        ttk.Label(master, text="Nombre Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.nombre_var, width=40).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Correo Electrónico:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.correo_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Confirmar Correo Electrónico:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.confirmar_correo_var, width=40).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Fecha de Nacimiento:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.fecha_nacimiento_var, width=40).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(master, text="Género:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.genero_var, width=40).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(master, text="Número de Teléfono:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.telefono_var, width=40).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(master, text="Dirección de Residencia:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.direccion_var, width=40).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(master, text="Ciudad de Residencia:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.ciudad_var, width=40).grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(master, text="País de Origen:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.pais_var, width=40).grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(master, text="Cargo Actual:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.cargo_var, width=40).grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(master, text="Áreas de Especialización:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.areas_especializacion_var, width=40).grid(row=10, column=1, padx=5, pady=5)

        ttk.Label(master, text="Objetivo o Meta a Corto Plazo:").grid(row=11, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.objetivo_meta_var, width=40).grid(row=11, column=1, padx=5, pady=5)

        ttk.Label(master, text="Contraseña:").grid(row=12, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.contrasena_var, width=40, show="*").grid(row=12, column=1, padx=5, pady=5)

        ttk.Label(master, text="Confirmar Contraseña:").grid(row=13, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(master, textvariable=self.confirmar_contrasena_var, width=40, show="*").grid(row=13, column=1, padx=5, pady=5)

        ttk.Button(master, text="Generar QR", command=self.generar_qr).grid(row=14, column=0, columnspan=2, pady=20)
        ttk.Button(master, text="Cargar Imagen de Fondo", command=self.cargar_imagen_fondo).grid(row=15, column=0, columnspan=2, pady=10)

        # Área para mostrar el código QR
        self.qr_frame = ttk.Frame(master)
        self.qr_frame.grid(row=16, column=0, columnspan=2, pady=10)
        self.qr_label = ttk.Label(self.qr_frame)
        self.qr_label.pack()

    def cargar_imagen_fondo(self):
        # Abrir el diálogo de archivos para seleccionar una imagen de fondo
        archivo_imagen = filedialog.askopenfilename(title="Seleccionar Imagen de Fondo", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])

        if archivo_imagen:
            # Cargar la imagen seleccionada
            self.fondo_imagen = Image.open(archivo_imagen)
            self.fondo_imagen = self.fondo_imagen.resize((600, 800))  # Redimensionar a tamaño de la ventana
            self.fondo_imagen_tk = ImageTk.PhotoImage(self.fondo_imagen)

            # Colocar la imagen de fondo en el canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.fondo_imagen_tk)
            self.canvas.image = self.fondo_imagen_tk  # Referencia para evitar que la imagen sea recogida por el garbage collector

    def generar_qr(self):
        # Obtener los datos de los campos
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        confirmar_correo = self.confirmar_correo_var.get()
        fecha_nacimiento = self.fecha_nacimiento_var.get()
        genero = self.genero_var.get()
        telefono = self.telefono_var.get()
        direccion = self.direccion_var.get()
        ciudad = self.ciudad_var.get()
        pais = self.pais_var.get()
        cargo = self.cargo_var.get()
        areas_especializacion = self.areas_especializacion_var.get()
        objetivo_meta = self.objetivo_meta_var.get()
        contrasena = self.contrasena_var.get()
        confirmar_contrasena = self.confirmar_contrasena_var.get()

        # Verificar que todos los campos estén llenos
        if not all([nombre, correo, confirmar_correo, fecha_nacimiento, genero, telefono, direccion,
                    ciudad, pais, cargo, areas_especializacion, objetivo_meta, contrasena, confirmar_contrasena]):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Verificar que los correos y contraseñas coincidan
        if correo != confirmar_correo:
            messagebox.showerror("Error", "Los correos electrónicos no coinciden.")
            return

        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Crear un identificador único
        id_unico = str(uuid.uuid4())

        # Crear el contenido del código QR
        qr_data = f"ID: {id_unico}\nNombre: {nombre}\nCorreo: {correo}\nFecha de Nacimiento: {fecha_nacimiento}\nGénero: {genero}\nTeléfono: {telefono}\nDirección: {direccion}\nCiudad: {ciudad}\nPaís: {pais}\nCargo: {cargo}\nÁreas de Especialización: {areas_especializacion}\nObjetivo: {objetivo_meta}"

        # Generar el código QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Convertir la imagen para mostrarla en tkinter
        qr_image = qr_image.resize((300, 300))
        qr_photo = ImageTk.PhotoImage(qr_image)

        # Mostrar el código QR
        self.qr_label.config(image=qr_photo)
        self.qr_label.image = qr_photo

        # Guardar el código QR como imagen
        qr_image.save(f"QR_{id_unico}.png")
        messagebox.showinfo("Éxito", f"Código QR generado y guardado como QR_{id_unico}.png")

        # Guardar los datos en un archivo de texto
        self.guardar_datos_en_txt(nombre, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais,
                                   cargo, areas_especializacion, objetivo_meta, id_unico)

    def guardar_datos_en_txt(self, nombre, correo, fecha_nacimiento, genero, telefono, direccion, ciudad, pais,
                              cargo, areas_especializacion, objetivo_meta, id_unico):
        archivo = "datos_qr.txt"
        
        if not os.path.exists(archivo):
            with open(archivo, 'w') as f:
                f.write("ID Único\tNombre\tCorreo\tFecha de Nacimiento\tGénero\tTeléfono\tDirección\tCiudad\tPaís\tCargo\tÁreas de Especialización\tObjetivo\n")
        
        with open(archivo, 'a') as f:
            f.write(f"{id_unico}\t{nombre}\t{correo}\t{fecha_nacimiento}\t{genero}\t{telefono}\t{direccion}\t{ciudad}\t{pais}\t{cargo}\t{areas_especializacion}\t{objetivo_meta}\n")


# Crear y ejecutar la aplicación
root = tk.Tk()
app = QRGeneratorApp(root)
root.mainloop()
