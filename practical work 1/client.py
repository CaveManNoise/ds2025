import socket

def ClientProgram():
    host = '127.0.0.1' #i set it to transfer in my machine but it can be adjusted to connect any remote host
    port = 5000  # configure the port to the same as host.py
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect((host, port))
    
    filename = 'recievedfile.txt'  #it should save the samepath with the file
    with open(filename, 'wb') as f:
        print(f"Receiving file from the server...")
        while True:
            data = ClientSocket.recv(1024)
            if not data:
                print("No more data received, closing connection.")
                break 
            f.write(data)  

    print(f"I got the file. it will be saved as {filename}")
    ClientSocket.close()

if __name__ == '__main__':
    ClientProgram()
