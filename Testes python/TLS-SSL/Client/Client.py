import socket
import ssl
import warnings

# Configuration
HOST = "127.0.0.1"
PORT = 12345

CERT_FILE = "certClient.crt"
KEY_FILE = "privateClient.key"
SERVER_CERT_FILE = "certServer.crt"

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Client:
    def __init__(self, serverAddress):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sslClientSocket = self.secureConnection(serverAddress)

        if self.sslClientSocket: self.communication()
        else: self.clientSocket.close()

    def secureConnection(self, serverAddress):
        try:
            sslSocket = ssl.wrap_socket(self.clientSocket, certfile=CERT_FILE, keyfile=KEY_FILE, ca_certs=SERVER_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)
            
            sslSocket.connect(serverAddress)
            print("\nConnection estabilished...\n")
 
            return sslSocket

        except Exception as e:
            print(f"\nConnection / Authentication ERROR: {e}\n")

    def communication(self):
        try:
            while True: self.requestHandler()

        except Exception as e:
            print(f"Communication ERROR: {e}\n") 

        finally:
            self.sslClientSocket.close()
            print("\nConnection closed...\n")

    def requestHandler(self):
        data = input("Type a message to the server: ")
        self.sslClientSocket.sendall(data.encode())

        serverResponse = self.sslClientSocket.recv(1024)
        print(f"\nServer answer \"{serverResponse.decode()}\"\n")


if __name__ == "__main__":
    print("Running...\n")
    client = Client((HOST, PORT))