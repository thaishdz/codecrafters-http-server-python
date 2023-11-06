
# Use curl to send custom HTTP requests and debug locally. Eg: curl -i -X GET http://localhost:4221/index.html

import socket


def main():
    
    HOST, PORT = "localhost", 4221

    server_socket = socket.create_server((HOST,PORT))
    connection_client, addr = server_socket.accept()

    print(f"Got a connection from {addr}")

    # Handle the connection - Here you can send/receive data, etc.
    #
    # receive data from the client
    data = connection_client.recv(1024)
    print(f"Received data {data.decode()}")
    url = data.decode()
    path = url.split(" ")[1]
    if path.startswith('/echo/'):
        response = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
        connection_client.send(response.encode()) # send a response back to the client
    elif path == '/':
        connection_client.send(b"HTTP/1.1 200 OK\r\n\r\n") 
        #
        # esta wea se manda en bytes porque 
        # usa sockets en este caso con conexion TCP 
        # para la comunicacion
        # 
    else:
        connection_client.send(b"HTTP/1.1 404 NOT FOUND\r\n\r\n") 


    # close the client socket
    connection_client.close()

if __name__ == "__main__":
    main()
