import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.13.224.226', 80)
server_socket.bind(server_address)

server_socket.listen(1)


client_socket, client_address = server_socket.accept()

try:
    filename = client_socket.recv(1024).decode()

    file_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file_data += data

    with open(filename, 'wb') as file:
        file.write(file_data)

except Exception as e:
    print(str(e))

finally:
    client_socket.close()
