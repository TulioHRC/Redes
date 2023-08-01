import socket
import ssl

# Configuration
HOST = "127.0.0.1"
PORT = 12345

CERT_FILE = "certServer.crt"
KEY_FILE = "privateServer.key"
CLIENTS_CERT_FILES = "certClient.crt"

class Server:
    def __init__(self, serverAddress):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(serverAddress)
        self.serverSocket.listen(5)
        print(f"Server on {serverAddress[0]}:{serverAddress[1]}")

        while True: self.mainLoop()

    def mainLoop(self):
        clientSocket, clientAddress = self.serverSocket.accept()
        print("\nConnection estabilished...\n")

        self.sslAuthenticatedSocket = self.authentication(clientSocket)

        if self.sslAuthenticatedSocket: self.communication()
        else: clientSocket.close()
        
    def authentication(self, clientSocket):
        try:
            sslSocket = ssl.wrap_socket(clientSocket, server_side=True, certfile=CERT_FILE, keyfile=KEY_FILE, ca_certs=CLIENTS_CERT_FILES, cert_reqs=ssl.CERT_REQUIRED)

            clientCerts = sslSocket.getpeercert()
            if clientCerts:
                print(f"Authentication Passed.\n{clientCerts['subject']}\n")
                return sslSocket

            print("Authentication Failed!!!")

        except Exception as e:
            print(f"Authentication ERROR: {e}\n")

    def communication(self):
        try:
            while True: self.requestHandler()

        except Exception as e:
            print(f"Communication ERROR: {e}\n") 

        finally:
            self.sslAuthenticatedSocket.close()
            print("\nConnection closed...\n")

    def requestHandler(self):
        data = self.sslAuthenticatedSocket.recv(1024)

        if data: 
            print(f"Message received: {data.decode()}")
            self.sslAuthenticatedSocket.sendall(f"Message return...".encode())


if __name__ == "__main__":
    print("Running...\n")
    server = Server((HOST, PORT))