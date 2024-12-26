import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import uuid
import os
import threading


class QRValidatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Validador de Códigos QR")
        master.geometry("600x500")

        # Crear interfaz gráfica para ingresar un código QR o verificar con cámara
        ttk.Label(master, text="Escanear Código QR").pack(pady=20)

        self.scan_button = ttk.Button(master, text="Escanear QR", command=self.start_camera_thread)
        self.scan_button.pack(pady=10)

        self.result_label = ttk.Label(master, text="Esperando escaneo...", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # Variable para almacenar la cámara
        self.cap = None
        self.running = False

        # Lista de cámaras disponibles
        self.cameras = self.get_available_cameras()

        # Interfaz para seleccionar la cámara
        self.camera_selection = ttk.Combobox(master, values=self.cameras, state="readonly")
        self.camera_selection.set(self.cameras[0] if self.cameras else "Ninguna")
        self.camera_selection.pack(pady=10)

    def get_available_cameras(self):
        """ Función para buscar las cámaras disponibles en el sistema """
        available_cameras = []
        for i in range(5):  # Vamos a probar los primeros 5 índices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
            cap.release()
        return available_cameras

    def start_camera_thread(self):
        """ Inicia un hilo para capturar imágenes desde la cámara sin bloquear la UI """
        if not self.running:
            self.running = True

            # Obtener el índice de la cámara seleccionada
            camera_index = int(self.camera_selection.get()) if self.camera_selection.get().isdigit() else 0

            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                return

            # Creamos un hilo para ejecutar la función de captura
            camera_thread = threading.Thread(target=self.capture_qr)
            camera_thread.daemon = True
            camera_thread.start()
        else:
            messagebox.showinfo("Información", "La cámara ya está en uso.")

    def capture_qr(self):
        """ Captura imágenes desde la cámara y procesa el QR """
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Detectar y decodificar códigos QR
            detector = cv2.QRCodeDetector()
            retval, decoded_info, points = detector.detectAndDecode(frame)

            # Si se detecta un código QR, procesamos los puntos
            if retval:
                # Verificar si 'points' es None o tiene el formato correcto
                if points is not None and len(points) > 0 and isinstance(points, list):
                    points = points[0]  # Tomamos el primer conjunto de puntos si hay más de uno
                    for i in range(len(points)):
                        # Dibuja las líneas alrededor del QR
                        cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 3)

                # Procesar el QR detectado
                self.process_qr_data(decoded_info)

                # Mostrar el texto de confirmación en la ventana
                cv2.putText(frame, "QR Detectado: " + decoded_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mostrar la imagen de la cámara en vivo
            cv2.imshow("Escaneando QR", frame)

            # Romper el loop si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def process_qr_data(self, qr_data):
        """ Procesa los datos del QR escaneado """
        # Verificar si el código QR existe en el archivo de datos
        if self.verify_qr_in_file(qr_data):
            # Suponemos que los datos están en el formato esperado: ID, Nombre, CI, Cargo, Número de Trabajador
            data_parts = qr_data.split("\n")
            if len(data_parts) >= 5:
                id_unico = data_parts[0]
                nombre = data_parts[1].split(":")[1].strip()
                ci = data_parts[2].split(":")[1].strip()
                cargo = data_parts[3].split(":")[1].strip()
                num_trabajador = data_parts[4].split(":")[1].strip()

                # Verificar los permisos según el cargo
                if cargo == "Obrero":
                    self.show_access("Acceso permitido a oficina principal y marcado de horario.")
                elif cargo == "Supervisor":
                    self.show_access("Acceso permitido a oficina principal, marcado de horario y planilla de obreros.")
                elif cargo == "Encargado de Sistemas":
                    self.show_access("Acceso total a los sistemas, puede modificar planillas.")
                elif cargo == "Director Regional":
                    self.show_access("Acceso completo, puede modificar sueldos y planillas con permiso del Director.")
                elif cargo == "Director":
                    self.show_access("Acceso completo sin restricciones.")
                else:
                    messagebox.showerror("Error", "Cargo no reconocido.")
            else:
                messagebox.showerror("Error", "Datos incompletos en el código QR.")
        else:
            messagebox.showerror("Error", "El código QR no es válido o no existe en el sistema.")

    def verify_qr_in_file(self, qr_data):
        """ Verifica si el código QR existe en el archivo de datos """
        archivo = "datos_qr.txt"
        if not os.path.exists(archivo):
            messagebox.showerror("Error", "El archivo de datos QR no existe.")
            return False

        # Verificar si el código QR está en el archivo
        with open(archivo, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if qr_data in line:
                    return True
        return False

    def show_access(self, message):
        """ Muestra el acceso permitido según el cargo """
        self.result_label.config(text=message)
        messagebox.showinfo("Acceso Permitido", message)


# Crear y ejecutar la aplicación
root = tk.Tk()
app = QRValidatorApp(root)
root.mainloop()
