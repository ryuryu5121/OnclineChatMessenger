import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

print('starting up on port {}'.format(server_port))

sock.bind((server_address, server_port))

clients = {}

while True:
    print('\nwaiting to receive message')

    data, server = sock.recvfrom(4096)
    name_length = int.from_bytes(data[:1], "big")
    clients[server] = server

    print('Received header from client. Byte lengths: Title length {}'.format(name_length))

    user_name = data[1:name_length + 1].decode('utf-8')
    message = data[name_length + 1:].decode('utf-8')
    print("{}: {} ".format(user_name, message))

    for client in clients:
        if client != server:
            sent = sock.sendto(data, client)
            print('sent {} bytes back to {}'.format(sent, client))


