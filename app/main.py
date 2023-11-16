import os
import socket
import threading
import argparse

def parse_argument():
   parser = argparse.ArgumentParser()
   parser.add_argument("--directory", required=True)
   args = parser.parse_args()
   return args.directory

def handle_response(content_type = None, data = None, status_code = 200):

    if status_code == 200:
        HEADER_HTTP = 'HTTP/1.1 200 OK'
        CRLF = '\r\n'
        CONTENT_TYPE = 'Content-Type: '
        CONTENT_LENGTH = 'Content-Length: '
        print(data)
        return f"{HEADER_HTTP}{CRLF}{CONTENT_TYPE}{content_type}{CRLF}{CONTENT_LENGTH}{len(data)}{CRLF}{CRLF}{data}".encode()
    else:
        HEADER_HTTP = 'HTTP/1.1 404 NOT FOUND'
        CRLF = '\r\n'
        CONTENT_TYPE = 'Content-Type: '
        CONTENT_LENGTH = 'Content-Length: '

        return f"{HEADER_HTTP}{CRLF}{CRLF}".encode()
        
def handle_file_request(directory,filename):
    # this line not working for me :(, I dunno why -> os.path.join(serving_directory, filename)
    filename = filename[1:]
    file_path = f"{directory}{filename}"  # Build the full file path
    if os.path.isfile(file_path):  # Check if the file exists
        with open(file_path, 'rb') as f:
            file_content = f.read().decode()
        return handle_response('application/octet-stream',file_content)
    else:
        return handle_response(status_code=404)

def handle_client(client_socket, addr):
    print(f"Got a connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024)
    print(f"Received data {data.decode()}")
    url = data.decode().split("\r\n")
    path = url[0].split(" ")[1]

    if path == '/':
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith('/echo/'): 
        response = handle_response('text/plain',path[6:])
    elif path == '/user-agent':
        user_agent = url[2].split(" ")[1]
        response = handle_response('text/plain',user_agent)
    elif path.startswith('/files'):
        filename = path.removeprefix('/files')
        directory = parse_argument()
        response = handle_file_request(directory,filename)
    else:
        response = handle_response(status_code=404)

    # Send the HTTP response back to the client
    client_socket.send(response)

    # Close the client socket
    client_socket.close()

def main():
    HOST, PORT = "localhost", 4221

    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen(5)  # Listen for incoming connections

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Accept incoming connections
        client_socket, addr = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
