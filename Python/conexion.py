import socket
import threading

class Conexion:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.lock = threading.Lock()

    def enviar_mensaje(self, mensaje):
        self.client_socket.sendall(mensaje)

    def recibir_mensaje(self):
        while True:
            try:
                mensaje = self.client_socket.recv(1024)
                if mensaje:
                    print(f"Mensaje recibido: {mensaje.decode('utf-8')}")
                    self.on_message_received(mensaje.decode('utf-8'))
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                break

    def on_message_received(self, mensaje):
        pass

    def cerrar(self):
        self.client_socket.close()