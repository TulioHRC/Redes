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

# Carregue o certificado do servidor para verificar a autenticidade
ssl_context.load_verify_locations(cafile="CA.crt")

# Carregue o certificado e a chave privada do cliente para autenticação
ssl_context.load_cert_chain(certfile="clientCA.crt", keyfile="privateClient.key")

# Inicie a comunicação TLS/SSL
ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=HOST)

# Conecta o cliente ao servidor
ssl_socket.connect(server_address)

# Mensagem que será enviada para o servidor
mensagem = "Olá, servidor!"

# Envia a mensagem para o servidor
ssl_socket.send(mensagem.encode())

# Recebe a resposta do servidor
resposta = ssl_socket.recv(1024)

print(f"Resposta do servidor: {resposta.decode()}")

# Fecha a conexão com o servidor
ssl_socket.close()
