const net = require('net');
const crypto = require('crypto');

// Clave de encriptación (debe ser la misma que la utilizada en los clientes)
const key = crypto.createHash('sha256').update('yLJHJo5hOzKMYROOTuRoQwLJfZx4W3hBRUYg4opoJZM=').digest();

const clients = [];
const allMessages = []; // Lista para almacenar todos los mensajes enviados

const server = net.createServer((socket) => {
    const clientId = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`Cliente conectado: ${clientId}`);
    clients.push(socket);

    // Enviar todos los mensajes almacenados si existen
    if (allMessages.length > 0) {
        socket.write("Mensajes Recibidos Hasta Ahora --->\n");
        allMessages.forEach(message => {
            socket.write(message + '\n');
        });
    }

    socket.on('data', (data) => {
        const encryptedMessage = data.toString();
        console.log('Mensaje encriptado recibido del cliente: ' + encryptedMessage);
        const decryptedMessage = decryptMessage(encryptedMessage);
        console.log('Mensaje desencriptado: ' + decryptedMessage);
        allMessages.push(encryptedMessage); // Almacenar el mensaje
        broadcastMessage(encryptedMessage, socket); // Enviar el mensaje encriptado a todos los clientes
    });

    socket.on('end', () => {
        console.log(`Cliente desconectado: ${clientId}`);
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
            if (client.writable) {
                client.write(message + '\n');
            }
        }
    });
}