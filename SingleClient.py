import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.24.236.171', 80)

client_socket.connect(server_address)

try:
    file_path = './LLBinary.bin'

    filename = file_path.split('/')[-1]

    client_socket.sendall(filename.encode())

    with open(file_path, 'rb') as file:
        file_data = file.read()
        client_socket.sendall(file_data)

    print("")

except Exception as e:
    print("", str(e))

finally:
    client_socket.close()
