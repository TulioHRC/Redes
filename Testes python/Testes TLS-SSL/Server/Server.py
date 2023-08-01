import socket
import ssl

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 12345
server_address = (HOST, PORT)
CERT_FILE = "CA.crt"
KEY_FILE = "privateServer.key"
CLIENT_CERT_FILE = "clientCA.crt"

# Faz o bind do socket ao endereço e porta do servidor
server_socket.bind(server_address)

# Define o número máximo de conexões em fila
server_socket.listen(5)

print(f"Servidor escutando em {HOST}:{PORT}")

while True:
    # Espera por uma conexão
    client_socket, client_address = server_socket.accept()

    print("\nConexão estabelecida...\n")

    # Inicie a comunicação TLS/SSL
    ssl_socket = ssl.wrap_socket(client_socket, server_side=True, certfile=CERT_FILE, keyfile=KEY_FILE, ca_certs=CLIENT_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)

    print("\nSSL socket criado.\n")

    # Verifique a autenticidade do certificado do cliente
    client_cert = ssl_socket.getpeercert()
    if not client_cert:
        print("Autenticação do cliente falhou.")
        continue

    print("Cliente autenticado:", client_cert['subject'])
    
    try:
        while True:
            # Recebe os dados enviados pelo cliente
            data = ssl_socket.recv(1024)

            # Processa os dados recebidos
            if data:
                print(f"Mensagem recebida do cliente: {data.decode()}")

            resposta = "Mensagem recebida."
            ssl_socket.sendall(resposta.encode())

    except Exception as e:
        print(f"\nErro: {e}\n\n")

    # Fecha a conexão com o cliente
    ssl_socket.close()


