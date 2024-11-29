import socket
import os

def ServerProgram():
    # Server host and port
    host = '127.0.0.1' 
    port = 5000

    SeverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SeverSocket.bind((host, port))
    
    SeverSocket.listen(1)#changee the number of connections if needed (i set 1 as default)
    print(f"Server listening on {host}:{port}...")
    conn, address = SeverSocket.accept()
    print(f"Connection from {address} has been established.")
    
    filename = r'E:\distrbuted system\task1\host\transfer_file.txt' 
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as file:
                print(f"Sending file: {filename}")
                while True:
                    data = file.read(1024)
                    if not data:
                        break  
                    conn.send(data)  
            print(f"File {filename} sent successfully!")
        except Exception as e: #error handling
            print(f"Error sending file: {e}")
            conn.send(b"Error sending file!")
    else:
        print(f"File {filename} not found!")
        conn.send(b"File not found!") 

    conn.close()
    SeverSocket.close()  

if __name__ == '__main__':
    ServerProgram()
