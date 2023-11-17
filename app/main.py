import os
import socket
import threading
import argparse

CRLF = '\r\n'

def parse_argument():
   parser = argparse.ArgumentParser()
   parser.add_argument("--directory", required=True)
   args = parser.parse_args()
   return args.directory

def handle_response(content_type = None, data = None, status_code = 200, message = 'OK'):
    HTTP_VERSION = 'HTTP/1.1'
    HTTP_HEADER = f'{HTTP_VERSION} {status_code} {message}'
    CONTENT_TYPE = 'Content-Type: '
    CONTENT_LENGTH = 'Content-Length: '
    if status_code == 200:
        if data == None:
            return f"{HTTP_HEADER}{CRLF}{CRLF}".encode()
        elif data:
            return f"{HTTP_HEADER}{CRLF}{CONTENT_TYPE}{content_type}{CRLF}{CONTENT_LENGTH}{len(data)}{CRLF}{CRLF}{data}".encode()
    if status_code == 201:
            return f"{HTTP_HEADER}{CRLF}{CONTENT_TYPE}{content_type}{CRLF}{CRLF}".encode()
    else:
        return f"{HTTP_HEADER}{CRLF}{CRLF}".encode()

def handle_file_request(directory,filename, http_method = 'GET', body = None):
    filename = filename[1:] # readme.txt
    file_path = os.path.join(directory, filename) # Build the full file path
    if os.path.isfile(file_path): # Check if the file exists
        with open(file_path, 'rb') as file:
            file_content = file.read().decode()
        return handle_response('application/octet-stream',file_content)

    if http_method == 'POST':
        with open(file_path, 'wb') as file:
            file.write(body.encode('ascii')) # convert to bytes
        return handle_response('application/octet-stream', status_code=201, message='CREATED')
    else:
        return handle_response(status_code=404, message='NOT FOUND')

def split_path(data):
    url = data.decode().split(CRLF)
    if len(url) >= 3:
        http_method = url[0].split(" ")[0] if len(url[0].split(" ")) >= 2 else '' # when request is ['GET / HTTP/1.1', '', '', '']
        path = url[0].split(" ")[1] if len(url[0].split(" ")) >= 2 else ''
        user_agent = url[2].split(" ")[1] if len(url[2].split(" ")) >= 2 else ''
        body = url[-1] if url[-1] != '' else ''
        return {'http_method': http_method, 'path': path, 'user_agent': user_agent, 'file_content': body}
    else:
        return {'http_method': None, 'path': None, 'user_agent': None}


def handle_client(client_socket, addr):
    print(f"Got a connection from {addr}{CRLF}")
    data = client_socket.recv(1024)   # Receive data from the client
    print(f"Received data {data.decode()}")

    http_method, path, user_agent, body = split_path(data).values()

    if path == '/':
        response = handle_response()
    elif path.startswith('/echo/'): 
        response = handle_response('text/plain',path[6:])
    elif path.startswith('/user-agent'):
        response = handle_response('text/plain',user_agent)
    elif path.startswith('/files'):
        filename = path.removeprefix('/files')
        directory = parse_argument()
        response = handle_file_request(directory,filename, http_method, body)
    else:
        response = handle_response(status_code=404, message='NOT FOUND')

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
