const net = require('net');
const crypto = require('crypto');

// Clave de encriptación (debe ser la misma que la utilizada en los clientes)
const key = crypto.createHash('sha256').update('yLJHJo5hOzKMYROOTuRoQwLJfZx4W3hBRUYg4opoJZM=').digest();

const clients = [];
const allMessages = []; // Almacena todos los mensajes enviados por los clientes

const server = net.createServer((socket) => {
    console.log('Cliente conectado');
    clients.push(socket);

    // Enviar todos los mensajes almacenados si existen
    if (allMessages.length > 0) {
        socket.write("Mensajes Recibidos Hasta Ahora --->\n");
        allMessages.forEach(encryptedMessage => {
            const decryptedMessage = decryptMessage(encryptedMessage);
            socket.write(decryptedMessage + '\n');
        });
    }

    socket.on('data', (data) => {
        const encryptedMessage = data.toString();
        console.log('Mensaje encriptado recibido del cliente: ' + encryptedMessage);
        const decryptedMessage = decryptMessage(encryptedMessage);
        console.log('Mensaje desencriptado: ' + decryptedMessage);
        allMessages.push(encryptedMessage); // Almacenar el mensaje
        broadcastMessage(decryptedMessage, socket);
    });

    socket.on('end', () => {
        console.log('Cliente desconectado');
        clients.splice(clients.indexOf(socket), 1);
    });

    socket.on('error', (error) => {
        console.error('Error: ', error);
    });
});

server.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000 :)');
});

function decryptMessage(encryptedMessage) {
    const encryptedBuffer = Buffer.from(encryptedMessage, 'base64');
    const nonce = encryptedBuffer.slice(0, 16);
    const tag = encryptedBuffer.slice(16, 32);
    const ciphertext = encryptedBuffer.slice(32);
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
    decipher.setAuthTag(tag);
    let decrypted = decipher.update(ciphertext, 'binary', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

function broadcastMessage(message, sender) {
    clients.forEach((client) => {
        if (client !== sender) {
            client.write(message);
        }
    });
}