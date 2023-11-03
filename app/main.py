
import socket


def main():
    
    HOST, PORT = "localhost", 4221

    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # bind the socket to the host and port
    server_socket.bind((HOST,PORT)) 

    # listen for incoming connections
    server_socket.listen(1) 

    print("Server is listening for incoming connections...")

    # accept a connection
    client_socket, addr = server_socket.accept()

    print(f"Got a connection from {addr}")

    # Handle the connection - Here you can send/receive data, etc.
    #
    # receive data from the client
    data = client_socket.recv(1024)
    print(f"Received data {data.decode()}")

    # send a response back to the client
    client_socket.send("HTTP/1.1 200 OK\r\n\r\n")

    # close the client socket
    client_socket.close()

if __name__ == "__main__":
    main()
