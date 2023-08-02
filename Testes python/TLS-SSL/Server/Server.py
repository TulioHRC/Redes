import socket
import ssl

# Configuration
HOST = "127.0.0.1"
PORT = 12345

CERT_FILE = "certServer.crt"
KEY_FILE = "privateServer.key"
CLIENT_CERT_FILE = "certClient.crt"

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
            sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            sslContext.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
            sslContext.load_verify_locations(cafile=CLIENT_CERT_FILE)
            sslContext.verify_mode = ssl.CERT_REQUIRED

            sslSocket = sslContext.wrap_socket(clientSocket, server_side=True)


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