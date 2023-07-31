import socket
import ssl

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 12345
server_address = (HOST, PORT)

# Faz o bind do socket ao endereço e porta do servidor
server_socket.bind(server_address)

# Define o número máximo de conexões em fila
server_socket.listen(5)

print(f"Servidor escutando em {HOST}:{PORT}")

# Use o socket como um contexto SSL (após a conexão inicial)
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="CA.crt", keyfile="privateServer.key")

# Exija a autenticação do cliente
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Carregue o certificado do cliente para verificar a autenticidade
ssl_context.load_verify_locations(cafile="clientCA.crt")

while True:
    # Espera por uma conexão
    client_socket, client_address = server_socket.accept()

    # Inicie a comunicação TLS/SSL
    ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

    # Verifique a autenticidade do certificado do cliente
    client_cert = ssl_socket.getpeercert()
    if not client_cert:
        print("Autenticação do cliente falhou.")
        continue

    print("Cliente autenticado:", client_cert['subject'])
    
    try:
        # Recebe os dados enviados pelo cliente
        data = ssl_socket.recv(1024)

        # Processa os dados recebidos
        if data:
            print(f"Mensagem recebida do cliente: {data.decode()}")

    except Exception as e:
        print(f"\nErro: {e}\n\n")

    # Fecha a conexão com o cliente
    ssl_socket.close()
