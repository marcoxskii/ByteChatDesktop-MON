# ByteChatDesktop

ByteChatDesktop es una aplicación de chat de escritorio basada en una arquitectura cliente-servidor. Permite a varios clientes conectarse a un servidor central para enviar y recibir mensajes de manera segura.

## Características

- **Arquitectura Cliente-Servidor**: Varios clientes pueden conectarse a un servidor central para enviar y recibir mensajes.
- **Sockets TCP**: Implementación de sockets TCP para la comunicación entre clientes y servidor.
- **Encriptación de Mensajes**: Los mensajes se encriptan utilizando `cryptography.fernet` para asegurar la integridad y confidencialidad de los datos.
- **Reconexión Automática**: Manejo de conexiones y desconexiones de los clientes, permitiendo la reconexión automática en caso de que un cliente se desconecte de la red.
- **Interfaz de Usuario Amigable**: Interfaz de usuario creada con `tkinter` que permite a los usuarios conectarse al servidor, enviar y recibir mensajes.
- **Sincronización de Mensajes**: Cuando un cliente se reconecta, recibirá todos los mensajes enviados por el servidor durante su desconexión para estar al día con la conversación.

## Requisitos

- Python 3.x
- Node.js
- Bibliotecas de Python: `tkinter`, `cryptography`

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu-usuario/ByteChatDesktop.git
   cd ByteChatDesktop
   ```

2. Instala las dependencias python:

    ```sh
    pip install cryptography
    ```

3. Instala Node.js si no lo tienes instalado:
En macOS
    ```sh
    # En macOS
    brew install node
    ```

## Uso

Servidor

1. Navega al directorio del servidor:
    ```sh
    cd DesktopSocket
    ```

2. Inicia el servidor
    ```sh
    node app.js
    ```

Cliente

1. Navega al directorio del cliente:
    ```sh
    cd Python
    ```

2. Inicia la aplicación del cliente:
    ```sh
    python main.py
    ```


