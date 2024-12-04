import socket
import threading
import base64
import sys
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

# Clave de encriptación (debe ser la misma que la utilizada en el servidor)
key = SHA256.new(b'yLJHJo5hOzKMYROOTuRoQwLJfZx4W3hBRUYg4opoJZM=').digest()

def encrypt_message(message):
    nonce = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

def decrypt_message(encrypted_message):
    encrypted_buffer = base64.b64decode(encrypted_message)
    nonce = encrypted_buffer[:16]
    tag = encrypted_buffer[16:32]
    ciphertext = encrypted_buffer[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted.decode('utf-8')

def receive_messages(client_socket):
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    # Limpiar la línea actual
                    sys.stdout.write('\r' + ' ' * 80 + '\r')
                    if message.startswith("Mensajes Recibidos Hasta Ahora --->"):
                        print(message)
                    else:
                        try:
                            decrypted_message = decrypt_message(message)
                            print(f"Recibido -> {decrypted_message}")
                        except Exception as e:
                            print(f"Error descifrando mensaje: {e}")
                            print(f"Mensaje cifrado -> {message}")
                    # Volver a mostrar el prompt
                    sys.stdout.write("Escribe tu mensaje: ")
                    sys.stdout.flush()
            else:
                break
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            break

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 3000))
    return client_socket

def main():
    name = input("Ingresa tu nombre: ")

    def handle_reconnection():
        while True:
            try:
                client_socket = connect_to_server()
                threading.Thread(target=receive_messages, args=(client_socket,)).start()
                break
            except (ConnectionRefusedError, OSError):
                print("Intentando reconectar...")
                time.sleep(5)

    client_socket = connect_to_server()
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    try:
        while True:
            message = input("Escribe tu mensaje: ")
            full_message = f"{name}: {message}"
            encrypted_message = encrypt_message(full_message)
            client_socket.send(encrypted_message.encode('utf-8'))
    except (BrokenPipeError, ConnectionResetError):
        print("Conexión perdida. Reconectando...")
        handle_reconnection()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        client_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    main()