import socket
import ssl

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 12345
server_address = (HOST, PORT)
CERT_FILE = "clientCA.crt"
KEY_FILE = "privateClient.key"
SERVER_CERT_FILE = "CA.crt"

# Cria um socket TCP para o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecte-se ao servidor
    ssl_socket = ssl.wrap_socket(client_socket, certfile=CERT_FILE, keyfile=KEY_FILE, ca_certs=SERVER_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)
    ssl_socket.connect(server_address)

    # Enviar e receber dados com o servidor através do ssl_socket
    while True:
        data_to_send = input("Digite uma mensagem para enviar ao servidor: ")
        ssl_socket.sendall(data_to_send.encode())

        data_received = ssl_socket.recv(1024)
        print("Resposta do servidor:", data_received.decode())
    
    ssl_socket.close()

except Exception as e:
    print("Erro:", e)

