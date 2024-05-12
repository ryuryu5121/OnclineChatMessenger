import socket
import threading
import sys
import json

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input("Type in the server's address to connect to :")
tcp_server_port = 9003
udp_server_port = 9002

def protocol_header(name_length):
    return name_length.to_bytes(1, "big")

def chatroom_protocol(room_name_size, operation, port, operation_pay_load_size):
    return room_name_size.to_bytes(1, "big") + operation.to_bytes(1, "big") + port.to_bytes(2, "big") + operation_pay_load_size.to_bytes(29, "big")

def receive_message(sock_udp):
    while True:
        try:
            data, address = sock_udp.recvfrom(1)
            if data:
                name_length = int.from_bytes(data, "big")
                data, address = sock_udp.recvfrom(4095)
                name = data[0:name_length].decode('utf-8')
                message = data[name_length:] .decode('utf-8')
                # print("\033[1A\033[1A") 
                print("\n{}: {} ".format(name, message))
            else:
                break
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break

def send_message():
    while True:
        try:
            message = input('input your message: ').encode('utf-8')
            if message == "exit":
                break
            message_length = len(message)
            sent = sock_udp.sendto(room_name_length.to_bytes(1, "big") + token_size.to_bytes(1, "big"), (server_address, udp_server_port))
            sent = sock_udp.sendto(room_name.encode('utf-8') + token.encode('utf-8') + message , (server_address, udp_server_port))
        except Exception as e:
            print(e)


try:
    sock_tcp.connect((server_address, tcp_server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    address = '0.0.0.0'
    port = int(input('your port: '))
    user_name = input('your name: ')
    user_name_length = len(user_name)
    sock_udp.bind((address, port))

    operation = int(input('please input number, 1:make a room , 2:enter the room: '))
    if operation == 1:
        room_name = input("input new RoomName: ")
    elif operation == 2:
        room_name = input("input you enter RoomName: ")
    room_name_length = len(room_name)
    
    sock_tcp.send(chatroom_protocol(room_name_length, operation, port, user_name_length))
    sock_tcp.send(room_name.encode('utf-8') + user_name.encode('utf-8'))
    length_bytes = sock_tcp.recv(2)
    message_len = int.from_bytes(length_bytes[:1], "big")
    token_size = int.from_bytes(length_bytes[1:], "big")
    message_from_server = sock_tcp.recv(message_len).decode('utf-8')
    token = sock_tcp.recv(token_size).decode('utf-8')

finally:
    sock_tcp.close()


receive_message_thread = threading.Thread(target=receive_message, args=(sock_udp,))
receive_message_thread.start()

send_message_thread = threading.Thread(target=send_message)
send_message_thread.start()
