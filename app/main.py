import socket
import threading

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
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
    elif path == '/user-agent':
        user_agent = url[2].split(" ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
    else:
        response = b"HTTP/1.1 404 NOT FOUND\r\n\r\n"

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
