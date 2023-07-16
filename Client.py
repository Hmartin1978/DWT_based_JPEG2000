import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.13.224.226', 80)

client_socket.connect(server_address)

try:
    file_path = './Len.bin'

    filename = file_path.split('/')[-1]

    client_socket.sendall(file_path.encode())

    with open(file_path, 'rb') as file:
        file_data = file.read()
        client_socket.sendall(file_data)


except Exception as e:
    print(str(e))

finally:
    client_socket.close()
