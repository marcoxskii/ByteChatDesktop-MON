import tkinter as tk
from tkinter import ttk
from datetime import datetime
from conexion import Conexion
from Crypto.Cipher import AES
import base64
import hashlib
import threading

# Variable para almacenar el nombre de usuario
username = None

# Crear una instancia de la clase Conexion
class ConexionConMensajes(Conexion):
    def on_message_received(self, mensaje):
        add_message(mensaje)

conexion = ConexionConMensajes()

# Clave de encriptación (debe ser la misma que la utilizada en el servidor)
key = 'yLJHJo5hOzKMYROOTuRoQwLJfZx4W3hBRUYg4opoJZM='  # Reemplaza esto con la clave generada
key = hashlib.sha256(key.encode()).digest()

# Función para encriptar el mensaje
def encrypt_message(message):
    print(f"Mensaje antes de encriptar: {message}")
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    encrypted_message = base64.b64encode(nonce + tag + ciphertext).decode('utf-8')
    print(f"Mensaje encriptado: {encrypted_message}")
    return encrypted_message

# Función para desencriptar el mensaje
def decrypt_message(encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    ciphertext = encrypted_message[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_message = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    return decrypted_message

# Función para enviar el mensaje
def send_message(event=None):
    global username
    message = entry.get()
    if not username:
        if message and message != "> Ingresa tu nombre de usuario:":
            username = message
            add_message(f"Bienvenido, {username}!")
            entry.delete(0, tk.END)
            entry.config(fg="orange")
            entry.insert(0, "")
    else:
        if message:
            full_message = f"{username}: {message}"
            encrypted_message = encrypt_message(full_message)
            conexion.enviar_mensaje(encrypted_message.encode('utf-8'))
            add_message(full_message)
            entry.delete(0, tk.END)

# Función para agregar un mensaje al contenedor
def add_message(message):
    message_label = tk.Label(messages_container, text=message, fg="orange", bg="black", font=("Courier", 12), anchor="w")
    message_label.pack(fill="x", pady=2, padx=5)

    # Scroll to the bottom
    messages_canvas.update_idletasks()
    messages_canvas.yview_moveto(1.0)

# Función para limpiar el campo de texto al hacer clic
def clear_entry(event):
    if entry.get() == "> Ingresa tu nombre de usuario:":
        entry.delete(0, tk.END)
        entry.config(fg="orange")

# Función para restaurar el mensaje de entrada si está vacío
def restore_entry(event):
    if not entry.get() and not username:
        entry.insert(0, "> Ingresa tu nombre de usuario:")
        entry.config(fg="gray")

# Crear la ventana principal
root = tk.Tk()

# Configurar el fondo de la ventana a color negro
root.configure(bg='black')

# Título de la ventana
root.title("ByteChat")

# Tamaño de la ventana
window_width = 1200
window_height = 700
root.geometry(f"{window_width}x{window_height}")

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición del centro
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Configurar la posición de la ventana
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Cargar la imagen
image = tk.PhotoImage(file="Python/bytechat.png")

# Crear un label con la imagen y darle un tamaño específico
label = tk.Label(root, image=image, bg="black")
label.place(x=window_width//2 - 150, y=10, width=300, height=150)  # Ajustar la posición y el tamaño

# Crear un contenedor con un canvas y una scrollbar para los mensajes
messages_frame = tk.Frame(root, bg="black")
messages_frame.place(x=10, y=170, width=window_width-20, height=window_height-200)  # Ajustar la posición y el tamaño

messages_canvas = tk.Canvas(messages_frame, bg="black", highlightbackground="orange", highlightthickness=1)
messages_canvas.pack(side="left", fill="both", expand=True)

# Estilo para la scrollbar
style = ttk.Style()
style.configure("Vertical.TScrollbar", background="black", bordercolor="white", arrowcolor="white")

scrollbar = ttk.Scrollbar(messages_frame, orient="vertical", command=messages_canvas.yview, style="Vertical.TScrollbar")
scrollbar.pack(side="right", fill="y")

messages_canvas.configure(yscrollcommand=scrollbar.set)

messages_container = tk.Frame(messages_canvas, bg="black")
messages_canvas.create_window((0, 0), window=messages_container, anchor="nw")

def on_configure(event):
    messages_canvas.configure(scrollregion=messages_canvas.bbox("all"))

messages_container.bind("<Configure>", on_configure)

# Crear un frame para el campo de texto y el botón
frame = tk.Frame(root, bg='black')
frame.pack(side="bottom", fill="x", padx=10, pady=20)

# Crear un campo de texto en la parte inferior de la ventana
entry = tk.Entry(frame, fg="gray", bg="black", insertbackground="orange", highlightbackground="orange", highlightcolor="orange", highlightthickness=1, relief="flat", font=("Courier", 12))
entry.insert(0, "> Ingresa tu nombre de usuario:")
entry.bind("<FocusIn>", clear_entry)
entry.bind("<FocusOut>", restore_entry)
entry.bind("<Return>", send_message)  # Vincular la tecla Enter a la función send_message
entry.pack(side="left", fill="x", expand=True)

# Crear un botón con el texto "Enviar" en la parte inferior de la ventana
button = tk.Button(frame, text="Send", fg="black", bg="orange", font=("Courier", 12), command=send_message)
button.pack(side="right")

# Iniciar un hilo para recibir mensajes
threading.Thread(target=conexion.recibir_mensaje, daemon=True).start()

# Ejecutar el bucle principal de la aplicación
root.mainloop()

# Cerrar la conexión al salir
conexion.cerrar()