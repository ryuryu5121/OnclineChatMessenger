import socket
import threading

def protocol_header(name_length):
    return name_length.to_bytes(1, "big")

def receive_message(sock):
    while True:
        try:
            data, address = sock.recvfrom(4096)
            name_length = int.from_bytes(data[:1], "big")
            name = data[1:name_length + 1].decode('utf-8')
            message = data[name_length + 1:] .decode('utf-8')
            print("{}: {} ".format(name, message))
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input("Type in the server's address to connect to :")
server_port = 9001

address = '0.0.0.0'
port = int(input('your port: '))
user_name = input('your name: ').encode('utf-8')
name_length = len(user_name).to_bytes(1, "big")

sock.bind((address, port))

message_thread = threading.Thread(target=receive_message, args=(sock,))
message_thread.start()

try:
    while True:
        message = input('input your message: ').encode('utf-8')
        message_length = len(message)
        print('sending {!r}'.format(message))
        sent = sock.sendto(name_length + user_name + message, (server_address, server_port))
        print('name:Send {} bytes'.format(sent))
finally:
    print('closing socket')
    sock.close()

