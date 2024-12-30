from xmlrpc.client import ServerProxy

def client_program():
    server = ServerProxy('http://127.0.0.1:5000/', allow_none=True)
    try:
        print("Requesting file from the server...")
        data = server.send_file()
        if isinstance(data, bytes):  # Check if the client got the file or not
            filename = 'received_file.txt'
            with open(filename, 'wb') as f:
                f.write(data)
            print(f"I got the file. It is saved as {filename}.")
        else:  # If not recieved, return an error messag
            print(f"Error from server: {data}")
    except Exception as e:
        print(f"Error during file transfer: {e}")

if __name__ == '__main__':
    client_program()
