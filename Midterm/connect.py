import socket
import threading

# Central Server Class
class CentralServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET <=> IPv4, SOCK_STREAM <=> TCP
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)  # Maximum 5 connections
        self.clients = {}  # Dictionary to store client connections

    def handle_client(self, client_socket, client_address):
        try:
            username = client_socket.recv(1024).decode()
            self.clients[username] = client_socket
            print(f"{username} connected from {client_address}")

            while True:
                message = client_socket.recv(1024).decode()
                if message == 'PEER':
                    client_socket.send(str(list(self.clients.keys())).encode())
                else:
                    self.broadcast(message, username)
        except:
            print(f"{username} disconnected.")
            del self.clients[username]
        finally:
            client_socket.close()

    def broadcast(self, message, username):
        for user, conn in self.clients.items():
            if user != username:
                try:
                    conn.send(f"{username}: {message}".encode())
                except:
                    continue

    def start(self):
        print("Central server started...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


# Peer-to-Peer Client Class
class PeerClient:
    def __init__(self, username, central_host='127.0.0.1', central_port=12345):
        self.username = username
        self.central_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.central_socket.connect((central_host, central_port))
        self.central_socket.send(username.encode())
        self.p2p_port = None  # Placeholder for P2P port

    def receive_messages(self):
        while True:
            try:
                message = self.central_socket.recv(1024).decode()
                print(message)
            except:
                print("Disconnected from server.")
                break

    def send_message(self, message):
        self.central_socket.send(message.encode())

    def peer_to_peer(self, peer_host, peer_port, message=None):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            if message:
                peer_socket.send(message.encode())
            threading.Thread(target=self.handle_peer, args=(peer_socket,)).start()
        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def handle_peer(self, peer_socket):
        while True:
            try:
                message = peer_socket.recv(1024).decode()
                print(f"Peer: {message}")
            except:
                print("Peer connection closed.")
                break

    def start_peer_listener(self, host='127.0.0.1', port=None):
        if port is None:
            port = int(input("Enter port for P2P listener (default is 54321): ") or 54321)
        self.p2p_port = port
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((host, port))
        listener_socket.listen(1)
        print(f"Listening for P2P connections on {host}:{port}...")
        while True:
            peer_socket, peer_address = listener_socket.accept()
            print(f"Connected to peer at {peer_address}")
            threading.Thread(target=self.handle_peer, args=(peer_socket,)).start()

    def start(self):
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.start_peer_listener, daemon=True).start()

        while True:
            message = input("Enter message (or 'PEER' for list): ")
            if message == 'PEER':
                self.send_message(message)
            elif message.startswith('P2P'):
                try:
                    parts = message.split(' ', 3)
                    if len(parts) < 4:
                        print("Invalid P2P command. Use: P2P <peer_host> <peer_port> <message>")
                        continue
                    _, peer_host, peer_port, peer_message = parts
                    self.peer_to_peer(peer_host, int(peer_port), peer_message)
                except ValueError:
                    print("Invalid P2P command. Use: P2P <peer_host> <peer_port> <message>")
            else:
                self.send_message(message)


# Main Execution
if __name__ == "__main__":
    choice = input("Enter 'server' to start as central server or 'client' to connect as client: ").strip().lower()

    if choice == 'server':
        server = CentralServer()
        server.start()
    elif choice == 'client':
        username = input("Enter your username: ").strip()
        client = PeerClient(username)
        client.start()
    else:
        print("Invalid choice.")
