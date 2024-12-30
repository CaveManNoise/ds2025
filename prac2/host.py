from xmlrpc.server import SimpleXMLRPCServer
import os

def send_file():
    filename = r'E:\distrbuted system\task2\host\transfer_file.txt'
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            print(f"File {filename} read successfully!")
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return f"Error reading file: {e}"
    else:
        print(f"File {filename} not found!")
        return "File not found!"

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('127.0.0.1', 5000), allow_none=True)
    print("RPC Server is listening on 127.0.0.1:5000...")
    server.register_function(send_file, 'send_file')
    server.serve_forever()
