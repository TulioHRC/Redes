import socket
import ssl

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 12345
server_address = (HOST, PORT)

# Cria um socket TCP para o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Usa o socket como um contexto SSL (para a negociação da conexão segura e seus parametros)
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Carregue o certificado e a chave privada do cliente para autenticação
ssl_context.load_cert_chain(certfile="clientCA.crt", keyfile="privateClient.key")

# Carregue o certificado do servidor para verificar a autenticidade
ssl_context.load_verify_locations(cafile="CA.crt")

try:
    # Conecte-se ao servidor
    ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=HOST)
    ssl_socket.connect(server_address)

    # Enviar e receber dados com o servidor através do ssl_socket
    while True:
        data_to_send = input("Digite uma mensagem para enviar ao servidor: ")
        ssl_socket.sendall(data_to_send.encode())

        data_received = ssl_socket.recv(1024)
        print("Resposta do servidor:", data_received.decode())

except Exception as e:
    print("Erro:", e)

finally:
    # Encerre a conexão
    ssl_socket.close()
