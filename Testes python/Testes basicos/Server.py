import socket

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
host = '127.0.0.1'
port = 12345
server_address = (host, port)

# Faz o bind do socket ao endereço e porta do servidor
server_socket.bind(server_address)

# Define o número máximo de conexões em fila
server_socket.listen(5)

print(f"Servidor escutando em {host}:{port}")

while True:
    # Espera por uma conexão
    client_socket, client_address = server_socket.accept()

    # Recebe os dados enviados pelo cliente
    data = client_socket.recv(1024)

    # Processa os dados recebidos
    if data:
        print(f"Mensagem recebida do cliente: {data.decode()}")

    # Fecha a conexão com o cliente
    client_socket.close()
